from datetime import datetime
from itertools import count

from models.base import BaseEntity
from models.people import Client
from models.vehicle import Vehicle


class Order(BaseEntity):
    _numbers = count(1)  # у заказов своя нумерация с 1

    def __init__(self, client, manager_login):
        super().__init__()
        self._number = next(Order._numbers)
        self.client = client
        self._manager_login = manager_login
        self._vehicles = []
        self._created_at = datetime.now()

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        if not isinstance(value, Client):
            raise TypeError("client должен быть Client")
        self._client = value

    @property
    def number(self):
        return self._number

    @property
    def manager_login(self):
        return self._manager_login

    @property
    def created_at(self):
        return self._created_at

    @property
    def vehicles(self):
        return tuple(self._vehicles)

    @property
    def total(self):
        return sum(v.price for v in self._vehicles)

    def add_vehicle(self, vehicle):
        if not isinstance(vehicle, Vehicle):
            raise TypeError("В заказ можно добавить только машину")
        if vehicle in self._vehicles:
            raise ValueError(f"{vehicle.title} уже есть в заказе")
        self._vehicles.append(vehicle)

    def identity(self):
        return (self._number,)

    def sort_key(self):
        return (self._created_at, self._number)

    def info(self):
        return f"Заказ N{self._number}: {self._client.name}, {len(self)} шт."

    # order + car
    def __add__(self, vehicle):
        self.add_vehicle(vehicle)
        return self

    def __len__(self):
        return len(self._vehicles)

    def __iter__(self):
        return iter(self._vehicles)

    def __contains__(self, vehicle):
        return vehicle in self._vehicles

    def __repr__(self):
        return f"Order(number={self._number}, client={self._client!r}, items={len(self)})"
