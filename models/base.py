from abc import ABC, abstractmethod
from functools import total_ordering
from itertools import count


# базовый класс для всех сущностей
@total_ordering
class BaseEntity(ABC):
    _counter = count(1)

    def __init__(self):
        self._id = next(BaseEntity._counter)

    @property
    def id(self):
        return self._id

    # по этому сравниваем на равенство
    @abstractmethod
    def identity(self):
        pass

    # по этому сортируем
    @abstractmethod
    def sort_key(self):
        pass

    @abstractmethod
    def info(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, BaseEntity):
            return NotImplemented
        return type(self) == type(other) and self.identity() == other.identity()

    def __lt__(self, other):
        if not isinstance(other, BaseEntity):
            return NotImplemented
        return self.sort_key() < other.sort_key()

    def __hash__(self):
        return hash((type(self).__name__, self.identity()))

    def __repr__(self):
        return f"{type(self).__name__}(id={self._id})"

    def __str__(self):
        return self.info()
