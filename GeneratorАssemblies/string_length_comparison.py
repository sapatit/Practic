import logging
from typing import Iterable, List

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def calculate_length_differences(first: Iterable[str], second: Iterable[str]) -> List[int]:
    """
    Вычисляет разницу длин строк из двух итерируемых объектов, если их длины не равны.

    :param first: Первый итерируемый объект строк.
    :param second: Второй итерируемый объект строк.
    :return: Список разниц длин строк.
    """
    differences = [len(f) - len(s) for f, s in zip(first, second) if len(f) != len(s)]
    logging.info(f"Calculated length differences: {differences}")
    return differences


def compare_string_lengths(first: Iterable[str], second: Iterable[str]) -> List[bool]:
    """
    Сравнивает длины строк в одинаковых позициях из двух итерируемых объектов.

    :param first: Первый итерируемый объект строк.
    :param second: Второй итерируемый объект строк.
    :return: Список булевых значений, указывающих на равенство длин.
    """
    max_length = max(len(first), len(second))
    comparisons = [len(first[i]) == len(second[i]) if i < len(first) and i < len(second) else False for i in
                   range(max_length)]
    logging.info(f"Compared string lengths: {comparisons}")
    return comparisons


# Основной код
first = ['Strings', 'Student', 'Computers']
second = ['Строка', 'Урбан', 'Компьютер']

first_result = calculate_length_differences(first, second)
second_result = compare_string_lengths(first, second)

# Вывод результатов
print(first_result)
print(second_result)
