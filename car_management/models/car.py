from dataclasses import dataclass, field
from car_management.validators.car_validators import validate_vin, validate_numbers
from car_management.exceptions.car_exceptions import IncorrectVinNumber, IncorrectCarNumbers


@dataclass(order=True)
class Car:
    """Базовый класс для представления автомобиля."""
    model: str
    vin: int
    numbers: str = field(compare=False)

    def __post_init__(self):
        validate_vin(self.vin)
        validate_numbers(self.numbers)

    def get_info(self) -> str:
        """Получить информацию об автомобиле."""
        return f'{self.model} с VIN: {self.vin} и номером: {self.numbers}'
