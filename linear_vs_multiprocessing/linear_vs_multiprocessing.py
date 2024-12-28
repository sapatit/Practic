import time
import logging
import rarfile
from multiprocessing import Pool
from tqdm import tqdm
from functools import wraps
import cProfile
import pstats
import io

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("process.log"),
        logging.StreamHandler()
    ]
)

# Флаг для отслеживания активного профилирования
profiling_active = False


def profile_logger(func):
    """Декоратор для профилирования функции."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        global profiling_active
        if profiling_active:
            return func(*args, **kwargs)  # Если профилирование уже активно, просто вызываем функцию

        pr = cProfile.Profile()
        pr.enable()  # Начинаем профилирование
        profiling_active = True  # Устанавливаем флаг
        result = func(*args, **kwargs)
        pr.disable()  # Останавливаем профилирование
        profiling_active = False  # Сбрасываем флаг

        # Сохраняем результаты профилирования в строковый поток
        s = io.StringIO()
        sortby = 'cumulative'  # Сортировка по кумулятивному времени
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()  # Печатаем статистику в поток

        # Логируем результаты
        logging.info(f"Профилирование функции '{func.__name__}':\n{s.getvalue()}")
        return result

    return wrapper


@profile_logger
def read_info(args):
    """Считывает строки из файла и возвращает их в виде списка."""
    filename, archive_path = args
    all_data = []
    with rarfile.RarFile(archive_path) as rf:
        with rf.open(filename) as f:
            # Читаем содержимое файла в память
            content = f.read()
            # Декодируем содержимое в нужной кодировке
            all_data = content.decode('utf-8').splitlines()  # Попробуйте 'windows-1251', если 'utf-8' не работает
    return all_data


def process_file(args):
    """Обрабатывает один файл."""
    return read_info(args)  # Передаем кортеж args напрямую


@profile_logger
def process_files(filenames, archive_path):
    """Обрабатывает файлы линейно и многопроцессно."""
    start_time = time.time()

    # Линейная обработка
    linear_results = []
    with rarfile.RarFile(archive_path) as rf:
        for filename in tqdm(filenames, desc="Линейный вызов", unit="файл"):
            data = read_info((filename, archive_path))
            linear_results.append(data)  # Сохраняем результаты
    linear_time = time.time() - start_time
    logging.info(f"Линейный вызов: {linear_time:.6f} секунд")

    # Многопроцессная обработка
    start_time = time.time()
    with Pool(processes=4) as pool:  # Увеличьте количество процессов, если это необходимо
        multiprocessing_results = list(tqdm(pool.imap(process_file, zip(filenames, [archive_path] * len(filenames))),
                                            total=len(filenames), desc="Многопроцессный вызов", unit="файл"))
    multiprocessing_time = time.time() - start_time
    logging.info(f"Многопроцессный вызов: {multiprocessing_time:.6f} секунд")

    # Объединяем результаты
    return linear_results, multiprocessing_results  # Возвращаем результаты


if __name__ == '__main__':
    archive_path = 'data/Files.rar'

    try:
        with rarfile.RarFile(archive_path) as rf:
            filenames = rf.namelist()
            process_files(filenames, archive_path)
    except FileNotFoundError:
        logging.error(f"Файл не найден: {archive_path}")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
