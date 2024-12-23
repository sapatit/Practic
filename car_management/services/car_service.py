from car_management.models.car import Car
from car_management.repositories.car_repository import CarRepository


class CarService:
    """Сервис для работы с автомобилями."""

    def __init__(self, repository: CarRepository):
        self.repository = repository

    def add_car(self, car: Car) -> None:
        """Добавить автомобиль в репозиторий."""
        self.repository.save(car)

    def get_all_cars(self) -> list:
        """Получить все автомобили."""
        return self.repository.get_all()
