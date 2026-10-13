from abc import ABC, abstractmethod


# общий предок для всех моих коллекций
class AbstractCollection(ABC):

    @abstractmethod
    def add(self, item):
        pass

    @abstractmethod
    def remove(self, item):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __len__(self):
        pass

    def is_empty(self):
        return len(self) == 0

    def __bool__(self):
        return not self.is_empty()

    def __repr__(self):
        return f"{type(self).__name__}(size={len(self)})"

    def __str__(self):
        return f"{type(self).__name__}: {len(self)} шт."
