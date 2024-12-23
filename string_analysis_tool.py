from typing import Sequence, Mapping, Iterator, Tuple, TypeVar
from collections import defaultdict
from dataclasses import dataclass

@dataclass
class StringLengthPair:
    first: str
    second: str

T = TypeVar('T', bound=str)

def filter_long_strings_lengths(strings: Sequence[T], min_length: int = 5) -> Iterator[int]:
    """Возвращает генератор длин строк, длина которых не менее min_length.

    Args:
        strings (Sequence[T]): Список строк для проверки.
        min_length (int): Минимальная длина строки.

    Yields:
        Iterator[int]: Длина строки, если она не менее min_length.
    """
    return (len(s) for s in strings if len(s) >= min_length)

def get_equal_length_pairs(list1: Sequence[str], list2: Sequence[str]) -> Iterator[StringLengthPair]:
    """Возвращает генератор пар строк одинаковой длины.

    Args:
        list1 (Sequence[str]): Первый список строк.
        list2 (Sequence[str]): Второй список строк.

    Yields:
        Iterator[StringLengthPair]: Генератор пар строк одинаковой длины.
    """
    length_map = defaultdict(list)
    for string in list2:
        length_map[len(string)].append(string)

    for first_string in list1:
        first_length = len(first_string)
        for second_string in length_map[first_length]:
            yield StringLengthPair(first_string, second_string)

def get_even_length_dict(strings: Sequence[str]) -> Mapping[str, int]:
    """Возвращает словарь, где ключ - строка, значение - длина строки для четных длин.

    Args:
        strings (Sequence[str]): Список строк для проверки.

    Returns:
        Mapping[str, int]: Словарь строк с четной длиной.
    """
    return {s: len(s) for s in strings if len(s) % 2 == 0}

def main() -> None:
    first_strings: Sequence[str] = ['Elon', 'Musk', 'Programmer', 'Monitors', 'Variable']
    second_strings: Sequence[str] = ['Task', 'Git', 'Comprehension', 'Java', 'Computer', 'Assembler']

    long_string_lengths: Iterator[int] = filter_long_strings_lengths(first_strings)
    equal_length_pairs: Iterator[StringLengthPair] = get_equal_length_pairs(first_strings, second_strings)
    even_length_dict: Mapping[str, int] = get_even_length_dict(first_strings + second_strings)

    print(f"Lengths of long strings: {list(long_string_lengths)}")
    print(f"Equal length pairs: {[(pair.first, pair.second) for pair in equal_length_pairs]}")
    print(f"Even length dictionary: {even_length_dict}")

if __name__ == "__main__":
    main()
