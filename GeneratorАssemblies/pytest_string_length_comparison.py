import pytest
from string_length_comparison import calculate_length_differences, compare_string_lengths

def test_calculate_length_differences():
    first = ['Strings', 'Student', 'Computers']
    second = ['Строка', 'Урбан', 'Компьютер']
    expected = [1, 2]  # Разница в длине строк
    result = calculate_length_differences(first, second)
    assert result == expected

def test_calculate_length_differences_no_differences():
    first = ['Same', 'Size', 'Test']
    second = ['Same', 'Size', 'Test']
    expected = []  # Нет разницы в длине
    result = calculate_length_differences(first, second)
    assert result == expected

def test_compare_string_lengths():
    first = ['Strings', 'Student', 'Computers']
    second = ['Строка', 'Урбан', 'Компьютер']
    expected = [False, False, True]  # Сравнение длин строк
    result = compare_string_lengths(first, second)
    assert result == expected

def test_compare_string_lengths_different_lengths():
    first = ['Short', 'LongerString', 'Equal']
    second = ['Tiny', 'Big', 'Equal']
    expected = [False, False, True]  # Сравнение длин строк
    result = compare_string_lengths(first, second)
    assert result == expected

def test_compare_string_lengths_empty():
    first = []
    second = []
    expected = []  # Оба списка пустые
    result = compare_string_lengths(first, second)
    assert result == expected

if __name__ == "__main__":
    pytest.main()
