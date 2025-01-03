import logging
import json
from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class FloorStatus(Enum):
    VALID = 1
    INVALID = 2


class InvalidHouseData(ValueError):
    """Ошибка, возникающая при некорректных входных данных для дома."""
    pass


class FloorNotFound(ValueError):
    """Ошибка, возникающая при попытке перейти на несуществующий этаж."""
    pass


class Observer(ABC):
    @abstractmethod
    def update(self, subject: 'House') -> None:
        pass


class HouseObserver(Observer):
    def update(self, subject: 'House') -> None:
        logging.info(f"Дом '{subject.name}' изменился: теперь он имеет {subject.number_of_floors} этажей.")


class FloorTransitionStrategy(ABC):
    @abstractmethod
    def go_to(self, current_floor: int, new_floor: int) -> None:
        pass


class DefaultFloorTransitionStrategy(FloorTransitionStrategy):
    def go_to(self, current_floor: int, new_floor: int) -> None:
        for floor in range(current_floor, new_floor + 1):
            logging.info(f"{floor}")
            print(f"{floor}")


class ReverseFloorTransitionStrategy(FloorTransitionStrategy):
    def go_to(self, current_floor: int, new_floor: int) -> None:
        for floor in range(new_floor, current_floor - 1, -1):
            logging.info(f"{floor}")
            print(f"{floor}")


class RandomFloorTransitionStrategy(FloorTransitionStrategy):
    import random

    def go_to(self, current_floor: int, new_floor: int) -> None:
        floors = list(range(current_floor, new_floor + 1))
        self.random.shuffle(floors)
        for floor in floors:
            logging.info(f"{floor}")
            print(f"{floor}")


@dataclass
class House:
    """Класс, представляющий дом с определенным количеством этажей."""
    name: str
    number_of_floors: int
    _is_locked: bool = False
    observers: List[Observer] = field(default_factory=list)
    floor_transition_strategy: FloorTransitionStrategy = field(default_factory=DefaultFloorTransitionStrategy)

    def __post_init__(self):
        if not isinstance(self.name, str) or not isinstance(self.number_of_floors, int) or self.number_of_floors <= 0:
            logging.error("Некорректные входные данные")
            raise InvalidHouseData("Некорректные входные данные")

    def __len__(self) -> int:
        """Возвращает количество этажей в доме."""
        return self.number_of_floors

    def __str__(self) -> str:
        """Возвращает строковое представление дома."""
        return f"Название: {self.name}, кол-во этажей: {self.number_of_floors}"

    @contextmanager
    def lock(self):
        try:
            self._is_locked = True
            yield
        finally:
            self._is_locked = False

    def add_observer(self, observer: Observer) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        self.observers.remove(observer)

    def notify_observers(self) -> None:
        for observer in self.observers:
            observer.update(self)

    def go_to(self, new_floor: int) -> FloorStatus:
        if self._is_locked:
            logging.warning("Невозможно перейти на другой этаж, дом заблокирован")
            raise FloorNotFound("Невозможно перейти на другой этаж, дом заблокирован")

        if new_floor < 1 or new_floor > self.number_of_floors:
            logging.warning(f"Такого этажа не существует")
            print(f"Такого этажа не существует")
            return FloorStatus.INVALID

        self.floor_transition_strategy.go_to(1, new_floor)
        return FloorStatus.VALID

    def set_number_of_floors(self, new_number_of_floors: int) -> None:
        if self._is_locked:
            logging.warning("Невозможно изменить количество этажей, дом заблокирован")
            raise FloorNotFound("Невозможно изменить количество этажей, дом заблокирован")

        if not isinstance(new_number_of_floors, int) or new_number_of_floors <= 0:
            logging.error("Некорректные входные данные")
            raise InvalidHouseData("Некорректные входные данные")

        self.number_of_floors = new_number_of_floors
        self.notify_observers()

    def save_state(self, filename: str) -> None:
        state = {
            'name': self.name,
            'number_of_floors': self.number_of_floors,
            '_is_locked': self._is_locked
        }
        with open(filename, 'w') as f:
            json.dump(state, f)
        logging.info(f"Состояние дома '{self.name}' сохранено в файл '{filename}'.")

    @classmethod
    def load_state(cls, filename: str) -> 'House':
        with open(filename, 'r') as f:
            state = json.load(f)
        house = cls(state['name'], state['number_of_floors'])
        house._is_locked = state['_is_locked']
        return house


def get_int_input(prompt: str, min_value: int = None, max_value: int = None) -> int:
    while True:
        try:
            value = int(input(prompt))
            if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                print(f"Пожалуйста, введите число от {min_value} до {max_value}.")
                continue
            return value
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите целое число.")


def main():
    logging.info("Запуск программы.")
    houses = []

    while True:
        print("\n1. Создать дом")
        print("2. Перейти на этаж")
        print("3. Изменить количество этажей")
        print("4. Сохранить состояние дома")
        print("5. Загрузить состояние дома")
        print("6. Вывести список домов")
        print("7. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            name = input("Введите название дома: ")
            number_of_floors = get_int_input("Введите количество этажей: ", min_value=1)
            house = House(name, number_of_floors)
            houses.append(house)
            house.add_observer(HouseObserver())
            logging.info(f"Создан дом: {house.name} с {house.number_of_floors} этажами.")

            # Вывод информации о доме
            print(f"Название дома: {house.name}, кол-во этажей: {house.number_of_floors}")
            print(f"Кол-во этажей в {house.name}: кол-во этажей {house.number_of_floors}")

        elif choice == '2':
            if not houses:
                print("Сначала создайте дом.")
                continue
            house_index = get_int_input(f"Выберите дом (0-{len(houses) - 1}): ", min_value=0, max_value=len(houses) - 1)
            new_floor = get_int_input("Введите номер этажа, на который хотите перейти: ", min_value=1,
                                      max_value=houses[house_index].number_of_floors)
            try:
                houses[house_index].go_to(new_floor)
            except (FloorNotFound, InvalidHouseData) as e:
                print(e)

        elif choice == '3':
            if not houses:
                print("Сначала создайте дом.")
                continue
            house_index = get_int_input(f"Выберите дом (0-{len(houses) - 1}): ", min_value=0, max_value=len(houses) - 1)
            new_number_of_floors = get_int_input("Введите новое количество этажей: ", min_value=1)
            try:
                houses[house_index].set_number_of_floors(new_number_of_floors)
            except (FloorNotFound, InvalidHouseData) as e:
                print(e)

        elif choice == '4':
            if not houses:
                print("Сначала создайте дом.")
                continue
            house_index = get_int_input(f"Выберите дом (0-{len(houses) - 1}): ", min_value=0, max_value=len(houses) - 1)
            filename = input("Введите имя файла для сохранения: ")
            houses[house_index].save_state(filename)

        elif choice == '5':
            filename = input("Введите имя файла для загрузки: ")
            try:
                house = House.load_state(filename)
                houses.append(house)
                house.add_observer(HouseObserver())
                logging.info(f"Загружен дом: {house.name} с {house.number_of_floors} этажами.")
                print(f"Название дома: {house.name}, кол-во этажей: {house.number_of_floors}")

            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Ошибка загрузки: {e}")

        elif choice == '6':
            if not houses:
                print("Список домов пуст.")
            else:
                print("Список домов:")
                for index, house in enumerate(houses):
                    print(f"{index}. Название дома: {house.name}, кол-во этажей: {house.number_of_floors}")

        elif choice == '7':
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()
