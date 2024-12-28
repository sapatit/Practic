import os
import pytest
import logging
from linear_vs_multiprocessing import read_info, process_file, process_files
import rarfile


@pytest.fixture(scope="function")  # Изменено на "function"
def setup_test_environment(tmp_path):
    """Создает тестовый RAR-архив для тестов."""
    test_dir = tmp_path / 'data'
    os.makedirs(test_dir, exist_ok=True)
    test_file = test_dir / 'test.txt'
    archive_path = test_dir / 'test.rar'

    # Создаем тестовый файл
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("Hello, World!\nThis is a test file.\n")

    # Создаем RAR-архив с помощью командной строки (например, с помощью WinRAR или 7-Zip)
    os.chdir(test_dir)
    os.system(f"rar a {archive_path.name} {test_file.name}")

    yield archive_path  # Возвращаем путь к архиву для тестов


def list_rar_contents(archive_path):
    with rarfile.RarFile(archive_path) as rf:
        return rf.namelist()


def test_read_info(setup_test_environment):
    """Тестируем функцию read_info."""
    archive_path = setup_test_environment
    result = read_info(('test.txt', archive_path))
    assert result == ["Hello, World!", "This is a test file."]


def test_process_file(setup_test_environment):
    """Тестируем функцию process_file."""
    archive_path = setup_test_environment
    result = process_file(('test.txt', archive_path))
    assert result == ["Hello, World!", "This is a test file."]


def test_process_files(setup_test_environment):
    """Тестируем функцию process_files."""
    archive_path = setup_test_environment
    print("Содержимое архива:", list_rar_contents(archive_path))  # Выводим содержимое архива
    linear_results, multiprocessing_results = process_files(['test.txt'], archive_path)
    assert linear_results is not None  # Проверяем, что линейные результаты не None
    assert multiprocessing_results is not None  # Проверяем, что многопроцессные результаты не None
    assert linear_results == multiprocessing_results  # Проверяем, что результаты совпадают
