from car_management.models.car import Car
from car_management.models.electric_car import ElectricCar
from car_management.services.car_service import CarService
from car_management.repositories.car_repository import CarRepository
from car_management.logging_config import setup_logging


def main():
    """Основная функция для создания автомобилей."""
    setup_logging('logging_config.yaml')

    # Создание репозитория и сервиса
    car_repository = CarRepository()
    car_service = CarService(car_repository)

    # Пример данных для автомобилей
    cars_data = [
        ('Model1', 1000001, 'f1234d'),  # Длина 6, корректный формат
        ('Model2', 1000002, 'т001тг'),  # Длина 6, корректный формат
        ('Model3', 2020202, 'abc123'),  # Длина 6, корректный формат
        ('ElectricModel1', 1000003, 'e12345', 75.0)  # Длина 6, корректный формат
    ]

    for data in cars_data:
        if len(data) == 3:  # Обычный автомобиль
            model, vin, numbers = data
            car = Car(model, vin, numbers)
        else:  # Электрический автомобиль
            model, vin, numbers, battery_capacity = data
            car = ElectricCar(model, vin, numbers, battery_capacity)

        car_service.add_car(car)

    # Получение всех автомобилей
    all_cars = car_service.get_all_cars()
    for car in all_cars:
        print(car.get_info())


if __name__ == "__main__":
    main()
