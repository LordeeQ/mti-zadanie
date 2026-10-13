from containers.custom_map import CustomMap
from models.people import User
from models.vehicle import Car, ElectricCar, Motorcycle, Truck


# начальные данные чтобы при запуске каталог не был пустой
class DataSeeder:

    @staticmethod
    def vehicles():
        return [
            Car("XTA21700080123456", "Lada", "Vesta", 2023, 1450000, "Белый", 4),
            Car("WVWZZZ1KZ8W123457", "Volkswagen", "Polo", 2021, 1690000, "Серый", 4),
            Car("JTDBR32E720123458", "Toyota", "Camry", 2024, 3990000, "Черный", 4),
            Car("WBA3A5C50CF123459", "BMW", "M4", 2022, 8750000, "Синий", 2),
            Car("KMHDN41AP4U123460", "Hyundai", "Solaris", 2020, 1250000, "Красный", 4),
            ElectricCar("5YJ3E1EA7KF123461", "Tesla", "Model 3", 2023, 4800000, "Белый", 510),
            ElectricCar("LGXCE6CB0N0123462", "BYD", "Han", 2024, 5200000, "Зеленый", 605),
            Truck("XTC65115083123463", "КАМАЗ", "65115", 2019, 6300000, "Оранжевый", 15),
            Truck("WDB9634031L123464", "Mercedes-Benz", "Actros", 2021, 12500000, "Серебристый", 20),
            Truck("X96330200B0123465", "ГАЗ", "Газель Next", 2022, 2900000, "Белый", 2),
            Motorcycle("JYARN23E9GA123466", "Yamaha", "MT-07", 2022, 950000, "Черный", 689),
            Motorcycle("ZDM1UB5V8KB123467", "Ducati", "Monster", 2023, 1850000, "Красный", 937),
            Motorcycle("1HD1KHM17KB123468", "Harley-Davidson", "Street Glide", 2021, 3200000, "Синий", 1868),
        ]

    @staticmethod
    def users():
        return [
            User("admin", "admin", "Администратор"),
            User("manager", "1234", "Иванов Иван"),
        ]

    # название типа -> класс, нужно в форме добавления
    @staticmethod
    def vehicle_types():
        types = CustomMap()
        for cls in (Car, ElectricCar, Truck, Motorcycle):
            types[cls.type_name()] = cls
        return types
