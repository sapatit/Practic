class CarException(Exception):
    """Базовый класс исключений для автомобилей."""
    pass


class IncorrectVinNumber(CarException):
    """Исключение для некорректного VIN номера."""

    def __init__(self, message: str) -> None:
        self.message = message


class IncorrectCarNumbers(CarException):
    """Исключение для некорректного номера автомобиля."""

    def __init__(self, message: str) -> None:
        self.message = message
