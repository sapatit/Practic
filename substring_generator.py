from typing import Iterator


def generate_substrings(text: str) -> Iterator[str]:
    """
    Генерирует все непустые подстроки переданной строки.

    :param text: Исходная строка
    :yield: Подстроки строки
    """
    length = len(text)

    for start in range(length):
        for end in range(start + 1, length + 1):
            yield text[start:end]


def all_variants(text: str) -> Iterator[str]:
    """
    Генератор, который возвращает все возможные непустые подпоследовательности
    переданной строки.

    :param text: Исходная строка
    :yield: Подпоследовательности строки
    :raises ValueError: Если text не является строкой
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    if not text:  # Обработка пустой строки
        return iter([])  # Возвращаем пустой генератор

    return generate_substrings(text)


# Пример использования функции
if __name__ == "__main__":
    try:
        a = all_variants("abc")
        for substring in a:
            print(substring)
    except ValueError as e:
        print(e)


# Примеры тестов
def test_all_variants():
    assert list(all_variants("abc")) == ['a', 'ab', 'abc', 'b', 'bc', 'c']
    assert list(all_variants("")) == []
    assert list(all_variants("a")) == ['a']
    assert list(all_variants("ab")) == ['a', 'ab', 'b']
    print("Все тесты пройдены.")


# Запуск тестов
test_all_variants()
