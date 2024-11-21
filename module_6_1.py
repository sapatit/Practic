import logging
from abc import ABC, abstractmethod
from enum import Enum

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class LivingBeingError(Exception):
    """Пользовательское исключение для ошибок, связанных с живыми организмами."""
    pass


class State(Enum):
    ALIVE = "alive"
    DEAD = "dead"
    FED = "fed"
    HUNGRY = "hungry"


class LivingBeing(ABC):
    """Абстрактный класс, представляющий живые организмы."""

    @abstractmethod
    def is_alive(self) -> bool:
        """Проверяет, жив ли организм."""
        pass

    @abstractmethod
    def is_edible(self) -> bool:
        """Проверяет, съедобен ли организм."""
        pass


class Animal(LivingBeing):
    """Класс, представляющий животных."""

    def __init__(self, name: str) -> None:
        self._state = State.ALIVE
        self.name: str = name
        logging.info(f"Создано животное: {self.name}")

    @property
    def alive(self) -> bool:
        return self._state == State.ALIVE

    @property
    def fed(self) -> bool:
        return self._state == State.FED

    def is_alive(self) -> bool:
        return self.alive

    def is_edible(self) -> bool:
        return False  # Животные не съедобны

    def recover(self) -> None:
        """Восстанавливает состояние животного."""
        self._state = State.ALIVE
        logging.info(f"{self.name} восстановился.")

    def eat(self, food: LivingBeing) -> None:
        """Позволяет животному поесть другой живой организм."""
        if not isinstance(food, LivingBeing):
            raise LivingBeingError(f"{self.name} не может есть {food}. Это не живой организм.")

        if food.is_edible():
            logging.info(f"{self.name} съел {food.name}.")
            self._state = State.FED
        else:
            logging.warning(f"{self.name} не стал есть {food.name}. Это не съедобно.")
            self._state = State.DEAD

    def __repr__(self) -> str:
        return f"Animal(name={self.name}, state={self._state})"


class NonEdiblePlant(LivingBeing):
    """Класс, представляющий несъедобные растения."""

    def __init__(self, name: str) -> None:
        self.name: str = name
        logging.info(f"Создано несъедобное растение: {self.name}")

    def is_alive(self) -> bool:
        return True

    def is_edible(self) -> bool:
        return False

    def __repr__(self) -> str:
        return f"NonEdiblePlant(name={self.name})"


class EdiblePlant(NonEdiblePlant):
    """Класс, представляющий съедобные растения."""

    def is_edible(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"EdiblePlant(name={self.name})"


class Carnivore(Animal):
    """Класс, представляющий хищников."""

    def is_edible(self) -> bool:
        return False  # Хищники не съедобны

    def eat(self, food: LivingBeing) -> None:
        """Позволяет хищнику поесть другой живой организм."""
        super().eat(food)  # Используем метод родительского класса для логирования
        if self.alive and food.is_edible():
            logging.info(f"{self.name} съел {food.name}.")
            self._state = State.FED
        elif self.alive:
            logging.warning(f"{self.name} не стал есть {food.name}. Это не съедобно.")
            self._state = State.DEAD


class Mammal(Carnivore):
    """Класс, представляющий млекопитающих."""
    pass


class Predator(Carnivore):
    """Класс, представляющий хищников."""
    pass


# Пример использования
if __name__ == "__main__":
    a1 = Predator('Волк с Уолл-Стрит')
    a2 = Mammal('Хатико')
    p1 = NonEdiblePlant('Цветик семицветик')
    p2 = EdiblePlant('Заводной апельсин')

    # Проверка состояния
    logging.info(f"Проверка состояния: {a1}, {p1}")
    print(a1)
    print(p1)
    print(f"{a1.name} жив: {a1.alive}, сыт: {a1.fed}")
    print(f"{a2.name} жив: {a2.alive}, сыт: {a2.fed}")

    # Действия
    try:
        a1.eat(p1)  # Попытка съесть несъедобное растение
        a2.eat(p2)  # Попытка съесть съедобное растение
    except LivingBeingError as e:
        logging.error(e)

    # Проверка состояния после действий
    logging.info(f"Состояние после действий: {a1}, {a2}")
    print(a1)
    print(a2)

    # Восстановление состояния
    a1.recover()
    logging.info(f"Состояние после восстановления: {a1}")
    print(a1)

    # Дополнительные проверки
    logging.info(f"Состояние {a1.name}: Жив: {a1.alive}, Сыто: {a1.fed}")
    logging.info(f"Состояние {a2.name}: Жив: {a2.alive}, Сыто: {a2.fed}")
