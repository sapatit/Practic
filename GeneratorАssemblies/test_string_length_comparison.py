import unittest
from string_length_comparison import calculate_length_differences, compare_string_lengths

class TestStringLengthComparison(unittest.TestCase):

    def test_calculate_length_differences(self):
        first = ['Strings', 'Student', 'Computers']
        second = ['Строка', 'Урбан', 'Компьютер']
        expected = [1, 2]  # Разница в длине строк
        result = calculate_length_differences(first, second)
        self.assertEqual(result, expected)

    def test_calculate_length_differences_no_differences(self):
        first = ['Same', 'Size', 'Test']
        second = ['Same', 'Size', 'Test']
        expected = []  # Нет разницы в длине
        result = calculate_length_differences(first, second)
        self.assertEqual(result, expected)

    def test_compare_string_lengths(self):
        first = ['Strings', 'Student', 'Computers']
        second = ['Строка', 'Урбан', 'Компьютер']
        expected = [False, False, True]  # Сравнение длин строк
        result = compare_string_lengths(first, second)
        self.assertEqual(result, expected)

    def test_compare_string_lengths_different_lengths(self):
        first = ['Short', 'LongerString', 'Equal']
        second = ['Tiny', 'Big', 'Equal']
        expected = [False, False, True]  # Сравнение длин строк
        result = compare_string_lengths(first, second)
        self.assertEqual(result, expected)

    def test_compare_string_lengths_empty(self):
        first = []
        second = []
        expected = []  # Оба списка пустые
        result = compare_string_lengths(first, second)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
