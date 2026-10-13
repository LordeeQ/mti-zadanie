import re
from datetime import datetime


# проверки для сеттеров, если что не так кидаем ValueError
class Validator:
    MIN_YEAR = 1950
    PHONE_RE = re.compile(r"^\+?\d[\d\s\-()]{9,17}$")
    LOGIN_RE = re.compile(r"^[A-Za-z0-9_]{3,20}$")
    VIN_RE = re.compile(r"^[A-HJ-NPR-Z0-9]{17}$")  # в vin нет букв I O Q

    @staticmethod
    def not_empty(value, field):
        value = str(value).strip()
        if not value:
            raise ValueError(f"Поле '{field}' не может быть пустым")
        return value

    @staticmethod
    def positive_number(value, field):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(f"Поле '{field}' должно быть больше нуля")
        return value

    @staticmethod
    def year(value):
        max_year = datetime.now().year + 1
        if not isinstance(value, int) or value < Validator.MIN_YEAR or value > max_year:
            raise ValueError(f"Год выпуска должен быть от {Validator.MIN_YEAR} до {max_year}")
        return value

    @staticmethod
    def phone(value):
        value = str(value).strip()
        if not Validator.PHONE_RE.match(value):
            raise ValueError("Неправильный номер телефона")
        return value

    @staticmethod
    def login(value):
        value = str(value).strip()
        if not Validator.LOGIN_RE.match(value):
            raise ValueError("Логин должен быть от 3 до 20 символов (латиница, цифры, _)")
        return value

    @staticmethod
    def vin(value):
        value = str(value).strip().upper()
        if not Validator.VIN_RE.match(value):
            raise ValueError("VIN должен быть из 17 символов, без букв I, O, Q")
        return value
