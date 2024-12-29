import random
import time
import logging
from threading import Thread, Event
from queue import Queue
from typing import List, Optional
from dataclasses import dataclass

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class Table:
    number: int
    guest: Optional['Guest'] = None

    def is_free(self) -> bool:
        """Проверяет, свободен ли стол."""
        return self.guest is None

class Guest(Thread):
    def __init__(self, name: str, stop_event: Event):
        super().__init__()
        self.name = name
        self.stop_event = stop_event
        self.has_left = False  # Состояние, покинул ли гость кафе

    def run(self):
        """Имитация времени, проведенного гостем за столом."""
        wait_time = random.randint(3, 10)
        logging.info(f"{self.name} ожидает {wait_time} секунд.")
        time.sleep(wait_time)
        self.has_left = True  # Гость покинул кафе
        self.stop_event.set()  # Устанавливаем событие завершения после еды

class Cafe:
    def __init__(self, tables: List[Table]):
        self.queue = Queue()
        self.tables = tables

    def guest_arrival(self, *guests: Guest):
        """Обрабатывает прибытие гостей в кафе."""
        for guest in guests:
            self._seat_guest(guest)

    def _seat_guest(self, guest: Guest):
        """Сажает гостя за свободный стол или ставит в очередь."""
        free_table = next((table for table in self.tables if table.is_free()), None)
        if free_table:
            free_table.guest = guest
            guest.start()
            logging.info(f"{guest.name} сел(-а) за стол номер {free_table.number}")
        else:
            self.queue.put(guest)
            logging.info(f"{guest.name} в очереди")

    def discuss_guests(self):
        """Обслуживает гостей, пока есть очередь или занятые столы."""
        while not self.queue.empty() or any(not table.is_free() for table in self.tables):
            for table in self.tables:
                self._check_table(table)

    def _check_table(self, table: Table):
        """Проверяет состояние стола и освобождает его, если гость ушел."""
        if table.guest and table.guest.has_left:
            logging.info(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
            logging.info(f"Стол номер {table.number} свободен")
            table.guest = None
            self._seat_next_guest(table)

    def _seat_next_guest(self, table: Table):
        """Сажает следующего гостя из очереди за свободный стол."""
        if not self.queue.empty():
            next_guest = self.queue.get()
            table.guest = next_guest
            next_guest.start()
            logging.info(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")

    def close_cafe(self):
        """Закрывает кафе, когда все гости покинут заведение."""
        while not self.queue.empty() or any(table.guest for table in self.tables):
            time.sleep(1)  # Ожидание, пока все гости не покинут кафе
        logging.info("Кафе закрыто. Все гости покинули заведение.")

# Конфигурация
NUM_TABLES = 5
GUEST_NAMES = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]

# Создание столов
tables = [Table(number) for number in range(1, NUM_TABLES + 1)]

# Создание гостей с событием завершения
guests = [Guest(name, Event()) for name in GUEST_NAMES]

# Заполнение кафе столами
cafe = Cafe(tables)

# Приём гостей
cafe.guest_arrival(*guests)

# Обслуживание гостей
cafe.discuss_guests()

# Закрытие кафе
cafe.close_cafe()
