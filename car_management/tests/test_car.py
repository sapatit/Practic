import unittest
from car_management.models.car import Car
from car_management.models.electric_car import ElectricCar
from car_management.exceptions.car_exceptions import IncorrectVinNumber, IncorrectCarNumbers
from car_management.repositories.car_repository import CarRepository
from car_management.services.car_service import CarService

class TestCar(unittest.TestCase):
    """Тесты для класса Car и ElectricCar."""

    def setUp(self):
        self.repository = CarRepository()
        self.service = CarService(self.repository)

    def test_valid_car_creation(self):
        """Тест на создание корректного автомобиля."""
        car = Car('Model1', 1234567, 'abc123')
        self.service.add_car(car)
        self.assertEqual(len(self.repository.get_all()), 1)

    def test_valid_electric_car_creation(self):
        """Тест на создание корректного электрического автомобиля."""
        electric_car = ElectricCar('ElectricModel1', 1234568, 'abc124', 75.0)
        self.service.add_car(electric_car)
        self.assertEqual(len(self.repository.get_all()), 1)

    def test_invalid_vin_type(self):
        """Тест на некорректный тип VIN номера."""
        with self.assertRaises(IncorrectVinNumber) as context:
            Car('Model2', 'not_a_number', 'abc123')
        self.assertEqual(str(context.exception), 'Некорректный тип vin номер: str, ожидается int')

    def test_invalid_vin_range(self):
        """Тест на некорректный диапазон VIN номера."""
        with self.assertRaises(IncorrectVinNumber) as context:
            Car('Model3', 999999, 'abc123')
        self.assertEqual(str(context.exception), 'Неверный диапазон для vin номера')

    def test_invalid_numbers_type(self):
        """Тест на некорректный тип номера автомобиля."""
        with self.assertRaises(IncorrectCarNumbers) as context:
            Car('Model4', 1234567, 123456)
        self.assertEqual(str(context.exception), 'Некорректный тип данных для номеров: int, ожидается str')

    def test_invalid_numbers_length(self):
        """Тест на некорректную длину номера автомобиля."""
        with self.assertRaises(IncorrectCarNumbers) as context:
            Car('Model5', 1234567, 'abc')
        self.assertEqual(str(context.exception), 'Неверная длина или формат номера')

    def test_invalid_numbers_format(self):
        """Тест на некорректный формат номера автомобиля."""
        with self.assertRaises(IncorrectCarNumbers) as context:
            Car('Model6', 1234567, 'abc1234')
        self.assertEqual(str(context.exception), 'Неверная длина или формат номера')

if __name__ == "__main__":
    unittest.main()

