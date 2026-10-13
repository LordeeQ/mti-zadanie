from abc import abstractmethod

from models.base import BaseEntity
from services.validator import Validator


class Vehicle(BaseEntity):

    def __init__(self, vin, brand, model, year, price, color):
        super().__init__()
        self.vin = vin
        self.brand = brand
        self.model = model
        self.year = year
        self.price = price
        self.color = color
        self._in_stock = True

    @property
    def vin(self):
        return self._vin

    @vin.setter
    def vin(self, value):
        self._vin = Validator.vin(value)

    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, value):
        self._brand = Validator.not_empty(value, "Марка")

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = Validator.not_empty(value, "Модель")

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = Validator.year(value)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = Validator.positive_number(value, "Цена")

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = Validator.not_empty(value, "Цвет")

    @property
    def in_stock(self):
        return self._in_stock

    @in_stock.setter
    def in_stock(self, value):
        self._in_stock = bool(value)

    @property
    def title(self):
        return f"{self._brand} {self._model}"

    # это переопределяют наследники
    @staticmethod
    @abstractmethod
    def type_name():
        pass

    @staticmethod
    @abstractmethod
    def extra_label():
        pass

    @property
    @abstractmethod
    def extra_value(self):
        pass

    @abstractmethod
    def extra_text(self):
        pass

    def identity(self):
        return (self._vin,)

    def sort_key(self):
        return (self._price, self._brand, self._model, self._year)

    def info(self):
        return f"{self.type_name()} {self.title} ({self._year}), {self._color}"

    # машины одинаковые если vin совпадает, даже если классы разные
    def __eq__(self, other):
        if not isinstance(other, Vehicle):
            return NotImplemented
        return self._vin == other._vin

    def __hash__(self):
        return hash(self._vin)

    # True если машину еще не продали
    def __bool__(self):
        return self._in_stock

    def __repr__(self):
        return (f"{type(self).__name__}(vin={self._vin!r}, brand={self._brand!r}, "
                f"model={self._model!r}, year={self._year}, price={self._price})")


class Car(Vehicle):

    def __init__(self, vin, brand, model, year, price, color, doors=4):
        super().__init__(vin, brand, model, year, price, color)
        self.doors = doors

    @property
    def doors(self):
        return self._doors

    @doors.setter
    def doors(self, value):
        if value not in (2, 3, 4, 5):
            raise ValueError("Дверей может быть от 2 до 5")
        self._doors = value

    @staticmethod
    def type_name():
        return "Легковой"

    @staticmethod
    def extra_label():
        return "Двери, шт."

    @property
    def extra_value(self):
        return self._doors

    def extra_text(self):
        return f"{self._doors} дв."


class ElectricCar(Car):

    def __init__(self, vin, brand, model, year, price, color, range_km=400, doors=4):
        super().__init__(vin, brand, model, year, price, color, doors)
        self.range_km = range_km

    @property
    def range_km(self):
        return self._range_km

    @range_km.setter
    def range_km(self, value):
        self._range_km = Validator.positive_number(value, "Запас хода")

    @staticmethod
    def type_name():
        return "Электромобиль"

    @staticmethod
    def extra_label():
        return "Запас хода, км"

    @property
    def extra_value(self):
        return self._range_km

    def extra_text(self):
        return f"{self._range_km} км"


class Truck(Vehicle):

    def __init__(self, vin, brand, model, year, price, color, payload=5):
        super().__init__(vin, brand, model, year, price, color)
        self.payload = payload

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        self._payload = Validator.positive_number(value, "Грузоподъемность")

    @staticmethod
    def type_name():
        return "Грузовик"

    @staticmethod
    def extra_label():
        return "Грузоподъемность, т"

    @property
    def extra_value(self):
        return self._payload

    def extra_text(self):
        return f"{self._payload} т"


class Motorcycle(Vehicle):

    def __init__(self, vin, brand, model, year, price, color, engine_cc=600):
        super().__init__(vin, brand, model, year, price, color)
        self.engine_cc = engine_cc

    @property
    def engine_cc(self):
        return self._engine_cc

    @engine_cc.setter
    def engine_cc(self, value):
        self._engine_cc = Validator.positive_number(value, "Объем двигателя")

    @staticmethod
    def type_name():
        return "Мотоцикл"

    @staticmethod
    def extra_label():
        return "Объем двигателя, куб.см"

    @property
    def extra_value(self):
        return self._engine_cc

    def extra_text(self):
        return f"{self._engine_cc} куб.см"
