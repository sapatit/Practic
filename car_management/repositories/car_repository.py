from car_management.models.car import Car


class CarRepository:
    """Репозиторий для хранения автомобилей."""

    def __init__(self):
        self.cars = []

    def save(self, car: Car) -> None:
        """Сохранить автомобиль."""
        self.cars.append(car)

    def get_all(self) -> list:
        """Получить все автомобили."""
        return self.cars
