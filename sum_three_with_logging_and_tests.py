import logging
import unittest

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_prime_number(n):
    """Проверяет, является ли число простым."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def is_prime(log_to_file=True):
    """Декоратор, который проверяет, является ли результат функции простым числом."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            message = "Простое" if is_prime_number(result) else "Составное"
            if log_to_file:
                logging.info(f"{result}: {message}")
                print(f"Логирование: {result}: {message}")  # Для отладки
            print(message)  # Вывод в консоль
            return result
        return wrapper
    return decorator

@is_prime(log_to_file=True)
def sum_three(a, b, c):
    """Складывает три числа и возвращает результат."""
    return a + b + c

# Пример использования
if __name__ == "__main__":
    result = sum_three(2, 3, 6)  # Ожидается вывод: "Простое" и результат 11
    print(result)

    result = sum_three(1, 1, 1)  # Ожидается вывод: "Составное" и результат 3
    print(result)

    result = sum_three(4, 4, 4)  # Ожидается вывод: "Составное" и результат 12
    print(result)

    result = sum_three(5, 5, 5)  # Ожидается вывод: "Составное" и результат 15
    print(result)

    result = sum_three(0, 0, 0)  # Ожидается вывод: "Составное" и результат 0
    print(result)

    result = sum_three(-1, -1, -1)  # Ожидается вывод: "Составное" и результат -3
    print(result)

# Тестирование
class TestSumThree(unittest.TestCase):
    def test_sum_three(self):
        self.assertEqual(sum_three(2, 3, 6), 11)
        self.assertEqual(sum_three(1, 1, 1), 3)
        self.assertEqual(sum_three(4, 4, 4), 12)
        self.assertEqual(sum_three(5, 5, 5), 15)
        self.assertEqual(sum_three(0, 0, 0), 0)
        self.assertEqual(sum_three(-1, -1, -1), -3)

    def test_is_prime_number(self):
        self.assertTrue(is_prime_number(2))
        self.assertTrue(is_prime_number(3))
        self.assertFalse(is_prime_number(4))
        self.assertTrue(is_prime_number(5))
        self.assertFalse(is_prime_number(9))
        self.assertFalse(is_prime_number(1))
        self.assertFalse(is_prime_number(0))
        self.assertFalse(is_prime_number(-3))

if __name__ == "__main__":
    unittest.main()
