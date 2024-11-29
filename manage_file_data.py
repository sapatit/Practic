import logging
import json
from typing import List, Dict, Tuple, Any
import os
import csv
import yaml
import xml.etree.ElementTree as ET

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class FileHandler:
    def __init__(self, file_name: str, mode: str = 'w', encoding: str = 'utf-8', newline: str = '\n',
                 create_if_not_exists: bool = True, overwrite: bool = False, buffering: int = -1):
        self.file_name = file_name
        self.mode = mode
        self.encoding = encoding
        self.newline = newline
        self.buffering = buffering
        self.create_if_not_exists = create_if_not_exists
        self.overwrite = overwrite
        self.file = None


    def __enter__(self):
        self.file = open(self.file_name, self.mode, encoding=self.encoding)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()

    def custom_write(self, strings: List[str]) -> Dict[Tuple[int, int], str]:
        """
        Записывает строки в файл и возвращает словарь с позициями строк.

        :param strings: Список строк для записи.
        :return: Словарь с позициями строк.
        """
        if not isinstance(strings, list) or not all(isinstance(s, str) for s in strings):
            raise ValueError("Аргумент 'strings' должен быть списком строк.")

        strings_positions = {}

        try:
            with open(self.file_name, self.mode, encoding=self.encoding) as file:
                for index, string in enumerate(strings, start=1):
                    byte_position = file.tell()
                    file.write(string + self.newline)
                    strings_positions[(index, byte_position)] = string
                    logging.info(f"Записана строка {index}: '{string}' на позиции {byte_position} байт.")
        except IOError as e:
            logging.error(f"Ошибка при записи в файл: {e}")
            return {}

        return strings_positions

    def file_exists(self) -> bool:
        return os.path.isfile(self.file_name)

    def delete_file(self) -> None:
        if self.file_exists():
            os.remove(self.file_name)
            logging.info(f"Файл {self.file_name} успешно удален.")
        else:
            logging.warning(f"Файл {self.file_name} не существует.")

    def read_file(self) -> List[str]:
        """Читает содержимое файла и возвращает список строк."""
        try:
            with open(self.file_name, 'r', encoding=self.encoding) as file:
                return [line.rstrip(self.newline) for line in file.readlines()]
        except IOError as e:
            logging.error(f"Ошибка при чтении файла: {e}")
            return []

    def write_json(self, data: Any) -> None:
        """Записывает данные в формате JSON."""
        try:
            with open(self.file_name, 'w', encoding=self.encoding) as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
                logging.info(f"Данные записаны в формате JSON в файл {self.file_name}.")
        except IOError as e:
            logging.error(f"Ошибка при записи JSON в файл: {e}")
        except (TypeError, ValueError) as e:
            logging.error(f"Ошибка при сериализации данных в JSON: {e}")

    def read_json(self) -> Any:
        """Читает данные из файла в формате JSON."""
        try:
            with open(self.file_name, 'r', encoding=self.encoding) as file:
                return json.load(file)
        except IOError as e:
            logging.error(f"Ошибка при чтении JSON из файла: {e}")
            return None
        except json.JSONDecodeError as e:
            logging.error(f"Ошибка декодирования JSON: {e}")
            return None

    def write_csv(self, data: List[Dict[str, Any]]) -> None:
        """Записывает данные в формате CSV."""
        try:
            with self:
                fieldnames = list(data[0].keys())
                writer = csv.DictWriter(self.file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            logging.info(f"Данные записаны в формате CSV в файл {self.file_name}.")
        except (IOError, csv.Error) as e:
            logging.error(f"Ошибка при записи CSV в файл: {e}")

    def read_csv(self) -> List[Dict[str, Any]]:
        """Читает данные из файла в формате CSV."""
        try:
            with self:
                reader = csv.DictReader(self.file)
                return list(reader)
        except (IOError, csv.Error) as e:
            logging.error(f"Ошибка при чтении CSV из файла: {e}")
            return []

    def write_yaml(self, data: Any) -> None:
        """Записывает данные в формате YAML."""
        try:
            with self:
                yaml.dump(data, self.file, allow_unicode=True, indent=4)
            logging.info(f"Данные записаны в формате YAML в файл {self.file_name}.")
        except (IOError, yaml.YAMLError) as e:
            logging.error(f"Ошибка при записи YAML в файл: {e}")

    def read_yaml(self) -> Any:
        """Читает данные из файла в формате YAML."""
        try:
            with self:
                return yaml.load(self.file, Loader=yaml.FullLoader)
        except (IOError, yaml.YAMLError) as e:
            logging.error(f"Ошибка при чтении YAML из файла: {e}")
            return None

    def write_xml(self, root_element: ET.Element) -> None:
        """Записывает данные в формате XML."""
        try:
            with self:
                tree = ET.ElementTree(root_element)
                tree.write(self.file, encoding=self.encoding, xml_declaration=True)
            logging.info(f"Данные записаны в формате XML в файл {self.file_name}.")
        except (IOError, ET.ParseError) as e:
            logging.error(f"Ошибка при записи XML в файл: {e}")

    def read_xml(self) -> ET.Element:
        """Читает данные из файла в формате XML."""
        try:
            with self:
                tree = ET.parse(self.file)
                return tree.getroot()
        except (IOError, ET.ParseError) as e:
            logging.error(f"Ошибка при чтении XML из файла: {e}")
            return None


# Пример использования класса
if __name__ == "__main__":
    info = [
        'Text for tell.',
        'Используйте кодировку utf-8.',
        'Because there are 2 languages!',
        'Спасибо!'
    ]

    file_handler = FileHandler('test.txt', mode='w', encoding='utf-8', newline='\n', buffering=1)

    try:
        result = file_handler.custom_write(info)
        for elem in result.items():
            print(elem)

        # Чтение файла
        lines = file_handler.read_file()
        print("Содержимое файла:")
        for line in lines:
            print(line)

        # Запись и чтение JSON
        json_data = {'messages': info}
        file_handler.write_json(json_data)

        # Чтение JSON
        loaded_data = file_handler.read_json()
        print("Данные, загруженные из JSON:")
        print(loaded_data)

    except ValueError as e:
        logging.error(f"Ошибка: {e}")
    except Exception as e:
        logging.error(f"Непредвиденная ошибка: {e}")
