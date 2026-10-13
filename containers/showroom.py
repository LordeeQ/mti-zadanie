from operator import attrgetter

from containers.base import AbstractCollection
from containers.custom_map import CustomMap


# каталог салона
class Showroom(AbstractCollection):
    # название сортировки: (по какому полю, по убыванию или нет)
    SORT_OPTIONS = CustomMap([
        ("Сначала дешевые", (attrgetter("price"), False)),
        ("Сначала дорогие", (attrgetter("price"), True)),
        ("Сначала новые", (attrgetter("year"), True)),
        ("Сначала старые", (attrgetter("year"), False)),
        ("По марке", (attrgetter("brand", "model"), False)),
    ])

    def __init__(self, vehicles=()):
        self._vehicles = []
        for v in vehicles:
            self.add(v)

    def add(self, vehicle):
        if vehicle in self._vehicles:
            raise ValueError(f"Машина с VIN {vehicle.vin} уже есть")
        self._vehicles.append(vehicle)

    def remove(self, vehicle):
        self._vehicles.remove(vehicle)

    def filter(self, text="", type_name=None, min_price=0, max_price=None,
               only_in_stock=False, sort_by=None):
        text = text.strip().lower()
        result = []
        for v in self._vehicles:
            if text and text not in f"{v.brand} {v.model} {v.color}".lower():
                continue
            if type_name and v.type_name() != type_name:
                continue
            if v.price < min_price:
                continue
            if max_price is not None and v.price > max_price:
                continue
            if only_in_stock and not v:
                continue
            result.append(v)

        if sort_by in self.SORT_OPTIONS:
            key, reverse = self.SORT_OPTIONS[sort_by]
            result.sort(key=key, reverse=reverse)
        else:
            result.sort()
        return result

    # сколько машин каждой марки в наличии
    def brand_stats(self):
        stats = CustomMap()
        for v in self._vehicles:
            if v:
                stats.increment(v.brand)
        return stats

    @property
    def in_stock_count(self):
        return len([v for v in self._vehicles if v])

    @property
    def max_price(self):
        if not self._vehicles:
            return 0
        return max(v.price for v in self._vehicles)

    def __getitem__(self, index):
        return self._vehicles[index]

    def __contains__(self, vehicle):
        return vehicle in self._vehicles

    def __iter__(self):
        return iter(self._vehicles)

    def __len__(self):
        return len(self._vehicles)


class Cart(AbstractCollection):

    def __init__(self):
        self._items = []

    def add(self, vehicle):
        if not vehicle:
            raise ValueError(f"{vehicle.title} уже продан")
        if vehicle in self._items:
            raise ValueError(f"{vehicle.title} уже в корзине")
        self._items.append(vehicle)

    def remove(self, vehicle):
        self._items.remove(vehicle)

    def clear(self):
        self._items.clear()

    @property
    def total(self):
        return sum(v.price for v in self._items)

    def __add__(self, vehicle):
        self.add(vehicle)
        return self

    def __getitem__(self, index):
        return self._items[index]

    def __contains__(self, vehicle):
        return vehicle in self._items

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)


# все продажи
class OrderBook(AbstractCollection):

    def __init__(self):
        self._orders = []

    def add(self, order):
        if len(order) == 0:
            raise ValueError("Заказ пустой")
        self._orders.append(order)

    def remove(self, order):
        self._orders.remove(order)

    @property
    def revenue(self):
        return sum(o.total for o in self._orders)

    def __iter__(self):
        # новые сверху
        return iter(sorted(self._orders, reverse=True))

    def __len__(self):
        return len(self._orders)


# пользователи хранятся в CustomMap по логину
class UserRegistry(AbstractCollection):

    def __init__(self, users=()):
        self._users = CustomMap()
        for u in users:
            self.add(u)

    def add(self, user):
        if user.login in self._users:
            raise ValueError(f"Пользователь {user.login} уже есть")
        self._users[user.login] = user

    def remove(self, user):
        del self._users[user.login]

    def authenticate(self, login, password):
        user = self._users.get(login.strip())
        if user is None or not user.check_password(password):
            raise PermissionError("Неверный логин или пароль")
        return user

    def __contains__(self, login):
        return login in self._users

    def __iter__(self):
        return iter(self._users.values())

    def __len__(self):
        return len(self._users)
