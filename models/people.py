from datetime import datetime

from models.base import BaseEntity
from services.validator import Validator


# сотрудник салона, который заходит в программу
class User(BaseEntity):

    def __init__(self, login, password, full_name):
        super().__init__()
        self.login = login
        self.password = password
        self.full_name = full_name

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        self._login = Validator.login(value)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if len(str(value)) < 4:
            raise ValueError("Пароль минимум 4 символа")
        self._password = str(value)

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        self._full_name = Validator.not_empty(value, "ФИО")

    def check_password(self, password):
        return self._password == password

    def identity(self):
        return (self._login,)

    def sort_key(self):
        return (self._login,)

    def info(self):
        return f"{self._full_name} ({self._login})"

    def __repr__(self):
        # пароль не показываем
        return f"User(login={self._login!r}, full_name={self._full_name!r})"


class Client(BaseEntity):

    def __init__(self, name, phone):
        super().__init__()
        self.name = name
        self.phone = phone

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = Validator.not_empty(value, "Имя клиента")

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = Validator.phone(value)

    def identity(self):
        return (self._name, self._phone)

    def sort_key(self):
        return (self._name, self._phone)

    def info(self):
        return f"{self._name}, тел. {self._phone}"

    def __repr__(self):
        return f"Client(name={self._name!r}, phone={self._phone!r})"


# сеанс работы: кто зашел, когда зашел и когда вышел (для отчета)
class UserSession(BaseEntity):
    TIME_FORMAT = "%d.%m.%Y %H:%M:%S"

    def __init__(self, login, time_in=None):
        super().__init__()
        self.login = login
        if time_in is None:
            time_in = datetime.now()
        self.time_in = time_in
        self._time_out = None

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        self._login = Validator.not_empty(value, "Логин")

    @property
    def time_in(self):
        return self._time_in

    @time_in.setter
    def time_in(self, value):
        if not isinstance(value, datetime):
            raise TypeError("time_in должен быть datetime")
        self._time_in = value

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, value):
        if not isinstance(value, datetime):
            raise TypeError("time_out должен быть datetime")
        if value < self._time_in:
            raise ValueError("Время выхода раньше времени входа")
        self._time_out = value

    @property
    def is_closed(self):
        return self._time_out is not None

    def close(self):
        self.time_out = datetime.now()

    def as_row(self):
        if self._time_out:
            time_out = self._time_out.strftime(self.TIME_FORMAT)
        else:
            time_out = "-"
        return (self._login, self._time_in.strftime(self.TIME_FORMAT), time_out)

    def identity(self):
        return (self._login, self._time_in)

    def sort_key(self):
        return (self._time_in, self._login)

    def info(self):
        login, time_in, time_out = self.as_row()
        return f"{login}: {time_in} - {time_out}"

    def __repr__(self):
        return f"UserSession(login={self._login!r}, time_in={self._time_in.strftime(self.TIME_FORMAT)!r})"
