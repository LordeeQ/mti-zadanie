from containers.base import AbstractCollection
from models.base import BaseEntity


# пара ключ-значение
class Pair(BaseEntity):

    def __init__(self, key, value):
        super().__init__()
        self._key = key
        self.value = value

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def identity(self):
        return (self._key, self._value)

    def sort_key(self):
        return (str(self._key),)

    def info(self):
        return f"{self._key}: {self._value}"

    # чтобы можно было писать key, value = pair
    def __iter__(self):
        yield self._key
        yield self._value

    def __hash__(self):
        return hash(self._key)

    def __repr__(self):
        return f"Pair({self._key!r}, {self._value!r})"


# своя замена dict, т.к. dict использовать нельзя
# внутри просто список пар, поиск перебором (для нас элементов мало, норм)
class CustomMap(AbstractCollection):

    def __init__(self, pairs=()):
        self._pairs = []
        for key, value in pairs:
            self.put(key, value)

    def _find(self, key):
        for pair in self._pairs:
            if pair.key == key:
                return pair
        return None

    def put(self, key, value):
        pair = self._find(key)
        if pair is None:
            self._pairs.append(Pair(key, value))
        else:
            pair.value = value

    def get(self, key, default=None):
        pair = self._find(key)
        if pair is None:
            return default
        return pair.value

    def add(self, item):
        key, value = item
        self.put(key, value)

    def remove(self, key):
        pair = self._find(key)
        if pair is None:
            raise KeyError(key)
        self._pairs.remove(pair)

    # для подсчета статистики
    def increment(self, key, step=1):
        self.put(key, self.get(key, 0) + step)

    def keys(self):
        return [p.key for p in self._pairs]

    def values(self):
        return [p.value for p in self._pairs]

    def items(self):
        return list(self._pairs)

    def __getitem__(self, key):
        pair = self._find(key)
        if pair is None:
            raise KeyError(key)
        return pair.value

    def __setitem__(self, key, value):
        self.put(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def __contains__(self, key):
        return self._find(key) is not None

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self._pairs)

    def __eq__(self, other):
        if not isinstance(other, CustomMap):
            return NotImplemented
        if len(self) != len(other):
            return False
        for key in self:
            if key not in other or other[key] != self[key]:
                return False
        return True

    # сравниваем по размеру
    def __lt__(self, other):
        if not isinstance(other, CustomMap):
            return NotImplemented
        return len(self) < len(other)

    __hash__ = None

    def __repr__(self):
        return f"CustomMap({[tuple(p) for p in self._pairs]!r})"

    def __str__(self):
        return "{" + ", ".join(p.info() for p in self._pairs) + "}"
