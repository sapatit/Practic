import os
import unittest
from home_task.StreamingToFiles.scripts.word_writer import write_words

class TestWriteWords(unittest.TestCase):

    def setUp(self):
        """Создаем временную директорию для тестов."""
        self.test_dir = 'test_word_files'
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        """Удаляем временную директорию после тестов."""
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)

    def test_write_words_creates_file(self):
        """Проверяем, что файл создается и содержит правильные данные."""
        file_name = os.path.join(self.test_dir, 'test_file.txt')
        word_count = 5
        write_words(word_count, file_name, delay=0)  # Устанавливаем задержку в 0 для быстрого тестирования

        # Проверяем, что файл создан
        self.assertTrue(os.path.exists(file_name))

        # Проверяем содержимое файла
        with open(file_name, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), word_count)
            for i in range(1, word_count + 1):
                self.assertEqual(lines[i - 1].strip(), f"Какое-то слово № {i}")

if __name__ == '__main__':
    unittest.main()
