import logging
from dataclasses import dataclass

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StepValueError(ValueError):
    """Исключение, выбрасываемое при неверном значении шага."""
    pass

@dataclass
class Iterator:
    start: int
    stop: int
    step: int = 1
    pointer: int = None

    def __post_init__(self) -> None:
        """Инициализация итератора."""
        if self.step == 0:
            logging.error('Шаг не может быть равен 0.')
            raise StepValueError(f'Шаг не может быть равен 0. Получено: {self.step}')
        self.pointer = self.start
        logging.info(f'Итератор инициализирован: start={self.start}, stop={self.stop}, step={self.step}')

    def __iter__(self) -> 'Iterator':
        """Сбросить итератор к начальному значению."""
        self.pointer = self.start
        logging.debug('Итератор сброшен к начальному значению.')
        return self

    def __next__(self) -> int:
        """Получить следующее значение итерации."""
        if (self.step > 0 and self.pointer > self.stop) or (self.step < 0 and self.pointer < self.stop):
            logging.info('Итерация завершена.')
            raise StopIteration
        current = self.pointer
        self.pointer += self.step
        logging.debug(f'Возвращаем текущее значение: {current}, следующий указатель: {self.pointer}')
        return current

    def reset(self) -> None:
        """Сбросить итератор к начальному значению."""
        self.pointer = self.start
        logging.info('Итератор сброшен.')

def main():
    try:
        iter1 = Iterator(100, 200, 0)
        for i in iter1:
            print(i, end=' ')
    except StepValueError as e:
        print(f'Ошибка: {e}')

    iter2 = Iterator(-5, 1)
    iter3 = Iterator(6, 15, 2)
    iter4 = Iterator(5, 1, -1)
    iter5 = Iterator(10, 1)

    print("\nИтерация iter2:")
    for i in iter2:
        print(i, end=' ')
    print()

    print("Итерация iter3:")
    for i in iter3:
        print(i, end=' ')
    print()

    print("Итерация iter4:")
    for i in iter4:
        print(i, end=' ')
    print()

    print("Итерация iter5:")
    for i in iter5:
        print(i, end=' ')
    print()

    # Пример использования метода reset
    iter6 = Iterator(1, 5)
    print("\nИтерация iter6:")
    for i in iter6:
        print(i, end=' ')
    print()

    iter6.reset()  # Сброс итератора
    print("После сброса:")
    for i in iter6:
        print(i, end=' ')
    print()

if __name__ == "__main__":
    main()
