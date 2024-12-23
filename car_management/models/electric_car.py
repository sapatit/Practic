from car_management.models.car import (Car)


class ElectricCar(Car):
    """Класс для представления электрического автомобиля."""

    def __init__(self, model: str, vin: int, numbers: str, battery_capacity: float):
        super().__init__(model, vin, numbers)
        self.battery_capacity = battery_capacity

    def get_info(self) -> str:
        """Получить информацию об электрическом автомобиле."""
        return f'{super().get_info()} и емкостью батареи: {self.battery_capacity} кВтч'
