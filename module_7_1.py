import json
from pathlib import Path
import logging
from dataclasses import dataclass, field, asdict
from typing import List, Optional, TypeVar

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class Product:
    name: str
    weight: float
    category: str

    def __post_init__(self):
        if self.weight < 0:
            raise ValueError("Вес не может быть отрицательным")

    def __str__(self):
        return f"{self.name}, {self.weight}, {self.category}"

    def __repr__(self):
        return f"Product(name={self.name}, weight={self.weight}, category={self.category})"

    def to_dict(self):
        """Преобразует объект Product в словарь для сериализации."""
        return asdict(self)


T = TypeVar('T', bound=Product)


class ProductManager:
    def __init__(self, file_name: str = 'products.json'):
        self.file_name = file_name
        self.products: List[Product] = self._load_products()

    def _load_products(self) -> List[Product]:
        """Загружает продукты из файла, если он существует."""
        file_path = Path(self.file_name)
        if not file_path.is_file():
            logger.info("Файл с продуктами не найден. Создание нового файла.")
            return []

        try:
            with file_path.open('r') as file:
                products_data = json.load(file)
                return [Product(**data) for data in products_data]
        except json.JSONDecodeError:
            logger.error("Ошибка чтения файла. Файл поврежден или содержит неверный формат.")
            return []
        except Exception as e:
            logger.exception(f"Произошла ошибка при загрузке продуктов: {e}")
            return []

    def _save_products(self):
        """Сохраняет список продуктов в файл."""
        file_path = Path(self.file_name)
        try:
            with file_path.open('w') as file:
                json.dump([product.to_dict() for product in self.products], file, indent=4)
            logger.info("Продукты успешно сохранены.")
        except Exception as e:
            logger.exception(f"Произошла ошибка при сохранении продуктов: {e}")

    def add_product(self, product: Product):
        """Добавляет новый продукт в магазин, если он еще не существует."""
        if self.find_product(product.name):
            logger.warning(f'Продукт {product.name} уже есть в магазине')
        else:
            self.products.append(product)
            logger.info(f'Продукт {product.name} добавлен в магазин.')
            self._save_products()

    def display_products(self):
        """Отображает все доступные продукты."""
        if self.products:
            for product in self.products:
                print(product)
        else:
            logger.info("Нет доступных продуктов.")

    def clear_products(self):
        """Очищает все продукты из магазина."""
        self.products.clear()
        self._save_products()
        logger.info("Все продукты были удалены.")

    def find_product(self, name: str) -> Optional[Product]:
        """Находит продукт по имени."""
        product = next((p for p in self.products if p.name == name), None)
        if product is None:
            logger.warning(f'Продукт {name} не найден.')
        return product

    def update_product(self, name: str, weight: Optional[float] = None, category: Optional[str] = None):
        """Обновляет информацию о продукте."""
        product = self.find_product(name)
        if product:
            if weight is not None:
                if weight < 0:
                    logger.error("Ошибка: вес не может быть отрицательным.")
                    return
                product.weight = weight
            if category is not None:
                product.category = category
            self._save_products()
            logger.info(f'Продукт {name} обновлен.')
        else:
            logger.warning(f'Продукт {name} не найден.')

    def find_by_category(self, category: str) -> List[Product]:
        """Находит все продукты по категории."""
        found_products = [product for product in self.products if product.category == category]
        if found_products:
            for product in found_products:
                print(product)
        else:
            logger.info(f"Нет продуктов в категории '{category}'.")


class Shop:
    def __init__(self, product_manager: ProductManager):
        self.product_manager = product_manager

    def menu(self):
        """Отображает меню и обрабатывает пользовательский ввод."""
        while True:
            print("\n--- Меню магазина ---")
            print("1. Добавить продукт")
            print("2. Показать все продукты")
            print("3. Обновить продукт")
            print("4. Очистить все продукты")
            print("5. Найти продукт по имени")
            print("6. Найти продукты по категории")
            print("7. Выйти")

            choice = input("Выберите действие (1-7): ")

            if choice == '1':
                name = input("Введите имя продукта: ")
                weight = input("Введите вес продукта: ")
                category = input("Введите категорию продукта: ")
                try:
                    weight = float(weight)
                    product = Product(name, weight, category)
                    self.product_manager.add_product(product)
                except ValueError:
                    logger.error("Ошибка: вес должен быть числом.")

            elif choice == '2':
                self.product_manager.display_products()

            elif choice == '3':
                name = input("Введите имя продукта для обновления: ")
                weight = input("Введите новый вес продукта (или оставьте пустым для пропуска): ")
                category = input("Введите новую категорию продукта (или оставьте пустым для пропуска): ")

                weight = float(weight) if weight else None
                self.product_manager.update_product(name, weight, category)

            elif choice == '4':
                self.product_manager.clear_products()

            elif choice == '5':
                name = input("Введите имя продукта для поиска: ")
                product = self.product_manager.find_product(name)
                if product:
                    print(product)
                else:
                    logger.warning(f"Продукт {name} не найден.")

            elif choice == '6':
                category = input("Введите категорию для поиска: ")
                self.product_manager.find_by_category(category)

            elif choice == '7':
                logger.info("Выход из программы.")
                print("Выход из программы.")
                break

            else:
                logger.error("Неверный выбор. Пожалуйста, выберите действие от 1 до 7.")


if __name__ == "__main__":
    product_manager = ProductManager()
    shop = Shop(product_manager)
    shop.menu()