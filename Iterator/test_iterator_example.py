import unittest
from iterator_example import Iterator, StepValueError

class TestIterator(unittest.TestCase):
    def test_step_zero(self):
        """Тест на случай, когда шаг равен 0."""
        with self.assertRaises(StepValueError):
            Iterator(0, 10, 0)

    def test_positive_iteration(self):
        """Тест на положительную итерацию."""
        iter_obj = Iterator(0, 5, 1)
        result = list(iter_obj)
        self.assertEqual(result, [0, 1, 2, 3, 4, 5])

    def test_negative_iteration(self):
        """Тест на отрицательную итерацию."""
        iter_obj = Iterator(5, 0, -1)
        result = list(iter_obj)
        self.assertEqual(result, [5, 4, 3, 2, 1, 0])

    def test_reset(self):
        """Тест на сброс итератора."""
        iter_obj = Iterator(0, 5, 1)
        list(iter_obj)  # Проходим итерацию
        iter_obj.reset()  # Сбрасываем
        result = list(iter_obj)  # Проходим итерацию снова
        self.assertEqual(result, [0, 1, 2, 3, 4, 5])

    def test_reverse_iteration(self):
        """Тест на итерацию в обратном направлении."""
        iter_obj = Iterator(10, 5, -1)
        result = list(iter_obj)
        self.assertEqual(result, [10, 9, 8, 7, 6, 5])

    def test_empty_iteration(self):
        """Тест на случай, когда итерация не должна возвращать значения."""
        iter_obj = Iterator(5, 1, 1)
        result = list(iter_obj)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
