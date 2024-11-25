import logging
from typing import Optional, List, Dict
from enum import Enum

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Color(Enum):
    BLUE = 'blue'
    RED = 'red'
    GREEN = 'green'
    BLACK = 'black'
    WHITE = 'white'


class OwnerExistsError(Exception):
    """Исключение, возникающее, когда владелец уже существует."""
    pass


class Vehicle:
    __owners: Dict[str, List['Vehicle']] = {}  # Словарь владельцев и их транспортных средств

    def __init__(self, owner: str, model: str, color: Color, engine_power: int):
        self.validate_owner(owner)
        self.owner: str = owner
        self.__model: str = model
        self.__engine_power: int = self.validate_engine_power(engine_power)
        self.__color: Color = color

        # Добавляем владельца и транспортное средство в словарь
        Vehicle.__owners.setdefault(owner, []).append(self)

        logging.info(f"Создан транспортное средство: {self.get_info()}")

    @classmethod
    def validate_owner(cls, owner: str) -> None:
        if owner in cls.__owners:
            logging.error(f"Владелец {owner} уже существует. Транспортное средство не создано.")
            raise OwnerExistsError(f"Владелец {owner} уже существует.")

    @staticmethod
    def validate_engine_power(engine_power: int) -> int:
        if engine_power <= 0:
            logging.error("Мощность двигателя должна быть положительным числом.")
            raise ValueError("Мощность двигателя должна быть положительным числом.")
        return engine_power

    @property
    def model(self) -> str:
        return self.__model

    @property
    def engine_power(self) -> int:
        return self.__engine_power

    @property
    def color(self) -> Color:
        return self.__color

    def get_horsepower(self) -> str:
        return f"Мощность двигателя: {self.__engine_power}"

    def print_info(self) -> None:
        print(self.get_info())

    def get_info(self) -> str:
        return f"Модель: {self.model}, {self.get_horsepower()}, Цвет: {self.color.value}, Владелец: {self.owner}"

    def set_color(self, new_color: Color) -> None:
        logging.info(f"Смена цвета с {self.__color.value} на {new_color.value}")
        self.__color = new_color

    def change_owner(self, new_owner: str) -> None:
        if new_owner == self.owner:
            logging.warning(f"Невозможно изменить владельца на того же самого: {new_owner}")
            return

        self.validate_owner(new_owner)

        # Удаляем транспортное средство из старого владельца
        Vehicle.__owners[self.owner].remove(self)
        if not Vehicle.__owners[self.owner]:
            del Vehicle.__owners[self.owner]

        # Устанавливаем нового владельца
        self.owner = new_owner
        Vehicle.__owners.setdefault(new_owner, []).append(self)

        logging.info(f"Владелец изменен на {new_owner}")

    @classmethod
    def get_owners(cls) -> Dict[str, List[str]]:
        """Возвращает словарь владельцев и их транспортных средств."""
        return {owner: [vehicle.model for vehicle in vehicles] for owner, vehicles in cls.__owners.items()}

    def __str__(self) -> str:
        """Возвращает строковое представление объекта Vehicle."""
        return self.get_info()


class Sedan(Vehicle):
    __PASSENGERS_LIMIT = 5

    def __init__(self, owner: str, model: str, color: Color, engine_power: int):
        super().__init__(owner, model, color, engine_power)

    def __str__(self) -> str:
        """Возвращает строковое представление объекта Sedan."""
        return f"{super().__str__()} (Седан, лимит пассажиров: {self.__PASSENGERS_LIMIT})"


# Пример использования
if __name__ == "__main__":
    try:
        vehicle1 = Sedan('Fedos', 'Toyota Mark II', Color.BLUE, 500)
        vehicle2 = Sedan('Fedos', 'Honda Accord', Color.RED, 300)  # Это вызовет ошибку
    except OwnerExistsError as e:
        print(e)

    # Изначальные свойства
    vehicle1.print_info()

    # Меняем свойства (в т.ч. вызывая методы)
    try:
        vehicle1.set_color(Color.BLACK)
        vehicle1.change_owner('Vasyok')  # Изменение владельца
    except OwnerExistsError as e:
        logging.error(f"Ошибка при изменении владельца: {e}")
    except ValueError as e:
        logging.error(f"Ошибка при изменении свойств: {e}")

    # Проверяем что поменялось
    vehicle1.print_info()

    # Получаем всех владельцев
    owners_info = Vehicle.get_owners()
    logging.info(f"Информация о владельцах: {owners_info}")
