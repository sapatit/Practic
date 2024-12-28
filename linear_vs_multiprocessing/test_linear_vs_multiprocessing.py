import unittest
import os
import rarfile
import tempfile
import logging

# Импортируем функции из вашего модуля
from linear_vs_multiprocessing import read_info, process_file, process_files


class TestRarFileProcessing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Указываем путь к существующему RAR-архиву для тестов."""
        cls.archive_path = 'data/test.rar'

    def test_read_info(self):
        """Тестируем функцию read_info."""
        result = read_info(('test.txt', self.archive_path))
        self.assertEqual(result, ["Hello, World!", "This is a test file."])

    def test_process_file(self):
        """Тестируем функцию process_file."""
        result = process_file(('test.txt', self.archive_path))
        self.assertEqual(result, ["Hello, World!", "This is a test file."])

    def test_process_files(self):
        """Тестируем функцию process_files."""
        linear_results, multiprocessing_results = process_files(['test.txt'], self.archive_path)
        self.assertIsNotNone(linear_results)  # Проверяем, что линейные результаты не None
        self.assertIsNotNone(multiprocessing_results)  # Проверяем, что многопроцессные результаты не None
        self.assertEqual(linear_results, multiprocessing_results)  # Проверяем, что результаты совпадают


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
