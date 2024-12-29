import threading
import logging
from time import sleep, time
import os
from tqdm import tqdm

# Определение абсолютных путей
base_dir = os.path.dirname(os.path.abspath(__file__))  # Получаем директорию скрипта
logs_dir = os.path.join(base_dir, '..', 'logs')  # Путь к директории logs
word_files_dir = os.path.join(base_dir, '..', 'word_files')  # Путь к директории word_files

# Настройка логирования
os.makedirs(logs_dir, exist_ok=True)  # Создание директории logs, если она не существует
logging.basicConfig(filename=os.path.join(logs_dir, 'execution_log.txt'), level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def write_words(word_count, file_name, delay=0.1):
    try:
        with open(file_name, 'w') as f:
            # Инициализация прогресс-бара
            for i in tqdm(range(1, word_count + 1), desc=f"Запись в {file_name}", unit="слово"):
                f.write(f"Какое-то слово № {i}\n")
                sleep(delay)
        logging.info(f"Завершилась запись в файл {file_name}")
    except Exception as e:
        logging.error(f"Ошибка при записи в файл {file_name}: {e}")


def run_write_tasks(tasks):
    threads = []
    for args in tasks:
        thread = threading.Thread(target=write_words, args=args)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def main():
    # Создание директорий, если они не существуют
    os.makedirs(word_files_dir, exist_ok=True)

    # Взятие текущего времени
    start_time = time()

    # Запуск функций с аргументами из задачи
    tasks = [
        (10, os.path.join(word_files_dir, 'word_list_example1.txt')),
        (30, os.path.join(word_files_dir, 'word_list_example2.txt')),
        (200, os.path.join(word_files_dir, 'word_list_example3.txt')),
        (100, os.path.join(word_files_dir, 'word_list_example4.txt'))
    ]

    for task in tasks:
        write_words(*task)

    # Взятие текущего времени
    end_time = time()
    logging.info(f"Работа функций {end_time - start_time:.6f} секунд")

    # Взятие текущего времени для потоков
    start_time_threads = time()

    # Запуск потоков
    thread_tasks = [
        (10, os.path.join(word_files_dir, 'word_list_example5.txt')),
        (30, os.path.join(word_files_dir, 'word_list_example6.txt')),
        (200, os.path.join(word_files_dir, 'word_list_example7.txt')),
        (100, os.path.join(word_files_dir, 'word_list_example8.txt'))
    ]

    run_write_tasks(thread_tasks)

    # Взятие текущего времени
    end_time_threads = time()
    logging.info(f"Работа потоков {end_time_threads - start_time_threads:.6f} секунд")


if __name__ == "__main__":
    main()
