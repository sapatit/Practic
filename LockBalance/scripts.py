import threading
import random
import time
import logging
from contextlib import contextmanager
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)

@contextmanager
def acquire_lock(lock):
    lock.acquire()
    try:
        yield
    finally:
        lock.release()

@dataclass
class Bank:
    balance: int = 0
    lock: threading.Lock = threading.Lock()

    def deposit(self, transactions=100, min_amount=50, max_amount=500):
        """Метод для пополнения баланса банка."""
        for _ in range(transactions):
            amount = random.randint(min_amount, max_amount)
            with acquire_lock(self.lock):
                self._update_balance(amount)
            time.sleep(0.001)

    def take(self, transactions=100, min_amount=50, max_amount=500):
        """Метод для снятия средств с баланса банка."""
        for _ in range(transactions):
            amount = random.randint(min_amount, max_amount)
            logging.info(f"Запрос на {amount}")
            with acquire_lock(self.lock):
                if amount <= self.balance:
                    self._withdraw(amount)
                else:
                    logging.warning("Запрос отклонён, недостаточно средств")
                    # Не блокируем поток, просто продолжаем
                    continue
            time.sleep(0.001)

    def _update_balance(self, amount):
        """Обновляет баланс, добавляя указанную сумму."""
        self.balance += amount
        logging.info(f"Пополнение: {amount}. Баланс: {self.balance}")

    def _withdraw(self, amount):
        """Снимает указанную сумму с баланса."""
        self.balance -= amount
        logging.info(f"Снятие: {amount}. Баланс: {self.balance}")

# Создаем объект класса Bank
bk = Bank()

# Создаем потоки для методов deposit и take
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

# Запускаем потоки
th1.start()
th2.start()

# Ждем завершения потоков
th1.join()
th2.join()

# Выводим итоговый баланс
print(f'Итоговый баланс: {bk.balance}')
