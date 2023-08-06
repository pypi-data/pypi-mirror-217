from .exceptions import UnsafeError, InvalidColumnValue
from .util import _script_load

run_if_ent_exists = _script_load('''
if redis.call('exists', KEYS[1]) == 1 then
    table.remove(KEYS[1], 1)
    if ARGV[1] == 'del_first' {
        redis.call('del', KEYS[1])
    }
    local call = {ARGV[1], unpack(KEYS)}
    for i=2, #ARGV do
        call[#call+1] = ARGV[i]
    end
    return cjson.encode({ok=redis.call(unpack(call))})
end

return cjson.encode({err='Missing base entity'})
''')

def _decode(w, d):
    if w.decode:
        return w.decode(d)
    return d

class Wrapper(object):
    __slots__ = 'key', 'entity', 'encode', 'decode'
    def __init__(self, key, entity, encode=None, decode=None):
        self.key = key
        self.entity = entity
        self.encode = encode
        self.decode = decode

    def _call(self, cmd, args=(), next=None, keys=()):
        arg = [cmd]
        if next:
            arg.append(next)
        arg.extend(args)

        r = run_if_ent_exists(self.entity._connection, [self.key] + keys, args)
        if r.get('err'):
            raise UnsafeError(r.get('err'))

        return r.get('ok')

    def _encode(self, d):
        if self._encode:
            if isinstance(d, tuple):
                return tuple(map(self.encode, d))
            return self.encode(d)
        return d

    def _decode(self, d):
        if self.decode:
            return self.decode(d)
        return d

class ListWrapper(Wrapper):
    """
    Try to emulate some of Deque behavior with end pushing / popping.
    """
    def __len__(self):
        return self._call('llen')

    def __getitem__(self, value):
        if isinstance(value, int):
            r = self._call('lrange', (value, value))
            if r:
                return r[0]
            raise IndexError
        raise ValueError("expected integer index, you provided %s"%(type(value),))

    def tolist(self):
        r = self._call('lrange', (0, -1))
        if r and self.decode:
            return list(map(self.decode, r))
        return r

    def pushleft(self, *vals):
        return self._call('lpush', self._encode(vals))

    def popleft(self):
        return self._decode(self._call('lpop'))

    def append(self, *vals):
        return self._call('rpush', self._encode(vals))

    def pop(self):
        return self._decode(self._call('rpop'))

    def _set(self, value):
        if not isinstance(value, list):
            raise InvalidColumnValue("can't assign non-list to a list")
        if not value:
            self._call('del')
            return 0
        return self._call('del_first', self._encode(tuple(value)), next='rpush')

class SetWrapper(Wrapper):
    def __len__(self):
        return self._call('scard')

    def toset(self):
        r = self._call('smembers')
        if r and self.decode:
            return set(map(self.decode, r))
        return r

    def __or__(self, other):
        if not isinstance(other, SetWrapper):
            raise TypeError("Can't union SetWrapper and {:r}".format(type(other)))
        return self._call('sunion', keys=[other.key])

    def __and__(self, other):
        if not isinstance(other, SetWrapper):
            raise TypeError("Can't intersect SetWrapper and {:r}".format(type(other)))
        return self._call('sinter', keys=[other.key])

    def __sub__(self, other):
        if not isinstance(other, SetWrapper):
            raise TypeError("Can't compute difference between SetWrapper and {:r}".format(type(other)))
        return self._call('sdiff', keys=[other.key])

    def add(self, *vals):
        return self._call('sadd', vals)

    def remove(self, *vals):
        return self._call('srem', vals)

    def pop(self, count=None):
        r = self._call('spop', () if count is None else (count,))
        if isinstance(r, list) and self.decode:
            return list(map(self.decode, r))
        return r


def make_dict(translate, convert):
    result = {}
    i = 0
    for i in range(0, len(result) - 1, 2):
        result[translate[i]] = conert(translate[i+1])
    return result


class HashWrapper(Wrapper):
    def __len__(self):
        return self._call('hlen')

    def todict(self):
        result = self._call('hgetall')
        if not isinstance(result, dict):
            # try to convert
            result = make_dict(result, lambda x: x)
            
        return result

    def __getitem__(self, key):
        return self._call('hget', key)

    def __setitem__(self, key, value):
        return self._call('hset', key, value)


class ZsetWrapper(Wrapper):
    def __len__(self):
        return self._call('zcard')

    def todict(self):
        result = self._call('zrange', (0, -1, 'withscores'))
        if not isinstance(result, dict):
            # try to convert
            result = make_dict(result, float)
        return result

    def __getitem__(self, key):
        """
        Args:
            int -> (member, score) item at that zrange index
            int,int -> range of items at that zrange as dict
            slice -> with steps of +/- 1, range of items in that slice as dict
            float,float -> range of items with those scores as dict
            string,bytes -> score of that member as float
        
        """
        if isinstance(key, (str, bytes)):
            ret = self._call('zscore', key)
            if ret:
                return float(ret)
            return
        
        start = stop = step = None
        method = 'zrange'
            
        if isinstance(key, slice):
            start = key.start
            stop = key.stop
            step = key.step

        elif isinstance(key, tuple):
            if isinstance(key[0], (int, float)):
                start, stop = key
                method = 'zrangebyscore' if isinstance(key[0], float) else method
            else:
                raise ValueError("unkown key type")
            
            step = 1 if start <= stop else -1

        elif isinstance(key, int):
            start = stop = key
            step = 1

        else:
            raise ValueError("unknown key type")
            
        if step not in (1, -1):
            raise ValueError("can only get ranges with step of 1 or -1")

        if (start < stop and step < 0) or (start > stop and step > 0):
            return {}

        if start < stop:
            result = self._call(method, (start, stop, 'withscores'))
        else:
            result = self._call(method[:1] + 'rev' + method[1:], (start, stop, 'withscores'))

        if isinstance(key, int):
            if result:
                result[1] = float(result[1])
            return result

        return make_dict(result, float)

    def __setitem__(self, key, value):
        return self._call('zadd', value, key)

    def update(self, members):
        to_add = []
        for member, score in members.items():
            to_add.append(score)
            to_add.append(member)
        return self._call('zadd', to_add)


