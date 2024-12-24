import logging
from random import choice
from typing import Any, List

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 1. Lambda-функция
first = 'Мама мыла раму'
second = 'Рамена мало было'

# Используем lambda-функцию для сравнения символов
compare_chars = lambda x, y: x == y
result = list(map(compare_chars, first, second))

logging.info(f'Результат сравнения символов: {result}')
print(result)


# 2. Замыкание
def get_advanced_writer(file_name: str, mode: str = 'a') -> callable:
    """Возвращает функцию для записи данных в файл."""

    def write_everything(*data_set: Any) -> None:
        if not data_set:
            logging.warning("Нет данных для записи.")
            return

        try:
            with open(file_name, mode, encoding='utf-8') as f:
                for data in data_set:
                    if isinstance(data, list):
                        f.write(' '.join(map(str, data)) + '\n')  # Записываем список как строку
                    else:
                        f.write(str(data) + '\n')  # Записываем каждое значение в новой строке
                    logging.info(f'Записано в файл {file_name}: {data}')
        except IOError as e:
            logging.error(f"Ошибка при записи в файл: {e}")

    return write_everything


# Пример использования
write = get_advanced_writer('example.txt', mode='w')  # 'w' для перезаписи
write('Это строчка', ['А', 'это', 'уже', 'число', 5, 'в', 'списке'])


# 3. Метод __call__
class MysticBall:
    """Класс для случайного выбора слова из коллекции."""

    def __init__(self, *words: str) -> None:
        self.words = list(words)

    def __call__(self) -> str:
        """Возвращает случайное слово из коллекции."""
        if not self.words:
            logging.warning("Список слов пуст.")
            return "Нет доступных слов."

        chosen_word = choice(self.words)
        logging.info(f'Случайно выбрано слово: {chosen_word}')
        return chosen_word

    def add_word(self, word: str) -> None:
        """Добавляет новое слово в коллекцию."""
        self.words.append(word)
        logging.info(f'Добавлено новое слово: {word}')

    def show_words(self) -> List[str]:
        """Возвращает список всех доступных слов."""
        return self.words


# Пример использования
first_ball = MysticBall('Да', 'Нет', 'Наверное')
first_ball.add_word('Определенно')

# Показать все доступные слова
logging.info(f'Все доступные слова: {first_ball.show_words()}')
print(first_ball.show_words())

# Случайный выбор слов
print(first_ball())
print(first_ball())
print(first_ball())
