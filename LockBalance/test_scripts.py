import unittest
import threading
import random
from time import sleep
from scripts import Bank


class TestBank(unittest.TestCase):

    def setUp(self):
        """Создаем новый объект Bank перед каждым тестом."""
        self.bank = Bank()

    def test_initial_balance(self):
        """Проверяем, что начальный баланс равен 0."""
        self.assertEqual(self.bank.balance, 0)

    def test_deposit(self):
        """Проверяем, что метод deposit корректно увеличивает баланс."""
        self.bank.deposit(transactions=10, min_amount=50, max_amount=100)
        self.assertGreater(self.bank.balance, 0)

    def test_take(self):
        """Проверяем, что метод take корректно уменьшает баланс."""
        self.bank.balance = 500  # Устанавливаем баланс для теста
        self.bank.take(transactions=5, min_amount=50, max_amount=100)
        self.assertLessEqual(self.bank.balance, 500)

    def test_take_insufficient_funds(self):
        """Проверяем, что метод take не позволяет снимать больше, чем есть на счете."""
        self.bank.balance = 100  # Устанавливаем баланс для теста
        initial_balance = self.bank.balance
        self.bank.take(transactions=10, min_amount=200, max_amount=300)
        self.assertEqual(self.bank.balance, initial_balance)  # Баланс не должен измениться

    def test_concurrent_deposit_and_take(self):
        """Проверяем, что одновременные операции deposit и take работают корректно."""
        self.bank.balance = 300  # Устанавливаем начальный баланс
        deposit_thread = threading.Thread(target=self.bank.deposit, args=(100, 50, 100))
        take_thread = threading.Thread(target=self.bank.take, args=(100, 50, 100))

        deposit_thread.start()
        take_thread.start()

        deposit_thread.join()
        take_thread.join()

        # Проверяем, что баланс не стал отрицательным
        self.assertGreaterEqual(self.bank.balance, 0)

if __name__ == '__main__':
    unittest.main()
