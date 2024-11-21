from functools import total_ordering
from dataclasses import dataclass
from typing import List, Dict, Optional


class HouseHistory:
    """Класс для хранения истории домов."""

    def __init__(self):
        self._history: List[str] = []

    def add_house(self, house_name: str) -> None:
        """Добавляет дом в историю, если его там еще нет."""
        if house_name in self._history:
            raise ValueError(f"Дом '{house_name}' уже существует в истории.")
        self._history.append(house_name)

    def remove_house(self, house_name: str) -> None:
        """Выводит сообщение о сносе дома, но не удаляет его из истории."""
        if house_name in self._history:
            print(f"{house_name} снесён, но он останется в истории.")
        else:
            print(f"Дом '{house_name}' не найден в истории.")

    def __str__(self) -> str:
        return ', '.join(self._history)

    def __iter__(self):
        return iter(self._history)

    def __len__(self) -> int:
        return len(self._history)


@total_ordering
@dataclass
class House:
    """Класс, представляющий дом."""

    name: str
    number_of_floors: int
    house_history: HouseHistory

    def __post_init__(self) -> None:
        """Добавляет дом в историю после его создания."""
        self.house_history.add_house(self.name)

    def go_to(self, new_floor: int) -> List[int]:
        """Возвращает список этажей до указанного этажа."""
        if not (1 <= new_floor <= self.number_of_floors):
            raise InvalidFloorError(f"Этаж {new_floor} не существует в доме '{self.name}'.")
        return list(range(1, new_floor + 1))

    @property
    def next_floor(self) -> Optional[int]:
        """Возвращает следующий этаж, если он существует."""
        return self.number_of_floors + 1 if self.number_of_floors > 0 else None

    @property
    def previous_floor(self) -> Optional[int]:
        """Возвращает предыдущий этаж, если он существует."""
        return self.number_of_floors - 1 if self.number_of_floors > 1 else None

    def __len__(self) -> int:
        return self.number_of_floors

    def __str__(self) -> str:
        return f"Дом '{self.name}' с {self.number_of_floors} этажами."

    def __repr__(self) -> str:
        return f"House(name={self.name}, number_of_floors={self.number_of_floors})"

    def __eq__(self, other) -> bool:
        if isinstance(other, House):
            return self.number_of_floors == other.number_of_floors
        return NotImplemented

    def __lt__(self, other) -> bool:
        if isinstance(other, House):
            return self.number_of_floors < other.number_of_floors
        return NotImplemented

    def __add__(self, value: int) -> 'House':
        if isinstance(value, int):
            return House(self.name, self.number_of_floors + value, self.house_history)
        return NotImplemented

    def __iadd__(self, value: int) -> 'House':
        if isinstance(value, int):
            self.number_of_floors += value
            return self
        return NotImplemented

    def get_info(self) -> Dict[str, str]:
        """Возвращает информацию о доме в виде словаря."""
        return {"name": self.name, "number_of_floors": self.number_of_floors}


class InvalidFloorError(Exception):
    """Исключение для ошибок, связанных с этажами."""
    pass


if __name__ == "__main__":
    house_history = HouseHistory()  # Создаем экземпляр истории домов

    try:
        h1 = House('ЖК Эльбрус', 10, house_history)
        print(house_history)

        h2 = House('ЖК Акация', 20, house_history)
        print(house_history)

        h3 = House('ЖК Матрёшки', 15, house_history)
        print(house_history)

        # Попытка удалить дом из истории
        house_history.remove_house('ЖК Акация')
        house_history.remove_house('ЖК Матрёшки')

        print(house_history)

        house_history.remove_house('ЖК Эльбрус')

        # Получение информации о доме
        print(h1.get_info())

        # Пример работы с этажами
        try:
            print(f"Этажи до 5: {h1.go_to(5)}")
            print(f"Следующий этаж: {h1.next_floor}")
            print(f"Предыдущий этаж: {h1.previous_floor}")
        except InvalidFloorError as e:
            print(e)

        # Пример добавления этажей
        h1 += 5
        print(f"После добавления этажей: {h1}")

        # Проверка на уникальность имен
        try:
            h4 = House('ЖК Эльбрус', 12, house_history)
        except ValueError as e:
            print(e)

        # Попытка создания дома с уникальным именем
        h5 = House('ЖК Лотос', 8, house_history)
        print(house_history)

        # Проверка информации о новом доме
        print(h5.get_info())

    except Exception as e:
        print(f"Произошла ошибка: {e}")
