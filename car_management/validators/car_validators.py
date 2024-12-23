import re
from car_management.exceptions.car_exceptions import IncorrectVinNumber, IncorrectCarNumbers


def validate_vin(vin_number: int) -> None:
    """Валидация VIN номера."""
    if not isinstance(vin_number, int):
        raise IncorrectVinNumber(f'Некорректный тип vin номер: {type(vin_number).__name__}, ожидается int')
    if vin_number < 1000000 or vin_number > 9999999:
        raise IncorrectVinNumber('Неверный диапазон для vin номера')


def validate_numbers(numbers: str) -> None:
    """Валидация номера автомобиля с использованием регулярных выражений."""
    if not isinstance(numbers, str):
        raise IncorrectCarNumbers(f'Некорректный тип данных для номеров: {type(numbers).__name__}, ожидается str')
    if len(numbers) != 6 or not re.match(r'^[a-zA-Zа-яА-Я0-9]+$', numbers):
        raise IncorrectCarNumbers('Неверная длина или формат номера')
