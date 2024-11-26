import math
from dataclasses import dataclass

@dataclass
class Color:
    r: int
    g: int
    b: int

    def __post_init__(self):
        if not all(0 <= value <= 255 for value in (self.r, self.g, self.b)):
            raise ValueError("Invalid color values. Must be integers between 0 and 255.")

class Figure:
    def __init__(self, color: Color, filled: bool = False, *sides):
        self._sides = list(sides)
        self.color = color
        self.filled = filled

    @property
    def sides(self):
        return self._sides

    @sides.setter
    def sides(self, new_sides):
        if self._is_valid_sides(new_sides):
            self._sides = list(new_sides)
        else:
            raise ValueError("Invalid sides. Must be positive numbers.")

    def _is_valid_sides(self, new_sides):
        return all(isinstance(side, (int, float)) and side > 0 for side in new_sides)

    def __len__(self):
        return sum(self._sides)

    def get_info(self):
        return {
            "color": self.color,
            "filled": self.filled,
            "sides": self.sides
        }

class Circle(Figure):
    def __init__(self, color: Color, radius=None, circumference=None):
        super().__init__(color, False, 0)
        if circumference is not None:
            self.radius = circumference / (2 * math.pi)
        elif radius is not None:
            self.radius = radius
        else:
            raise ValueError("Either radius or circumference must be provided.")

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("Radius must be positive.")
        self._radius = value
        self.sides = [self.get_circumference()]

    def get_circumference(self):
        return 2 * math.pi * self.radius

    def get_area(self):
        return math.pi * (self.radius ** 2)

class Triangle(Figure):
    def __init__(self, a, b, c, color: Color):
        if not self._is_valid_triangle(a, b, c):
            raise ValueError("Invalid triangle sides.")
        super().__init__(color, False, a, b, c)

    @staticmethod
    def _is_valid_triangle(a, b, c):
        return a + b > c and a + c > b and b + c > a

    def get_area(self):
        s = sum(self.sides) / 2  # Semi-perimeter
        return math.sqrt(s * (s - self.sides[0]) * (s - self.sides[1]) * (s - self.sides[2]))

class Cube(Figure):
    def __init__(self, color: Color, edge_length):
        super().__init__(color, False, *([edge_length] * 12))
        self.edge_length = edge_length

    @property
    def edge_length(self):
        return self._edge_length

    @edge_length.setter
    def edge_length(self, value):
        if value <= 0:
            raise ValueError("Edge length must be positive.")
        self._edge_length = value
        self.sides = [value] * 12

    def get_volume(self):
        return self.edge_length ** 3

    def get_sides(self):
        return [self.edge_length] * 12

if __name__ == "__main__":
    circle1 = Circle(Color(200, 200, 100), radius=10)
    cube1 = Cube(Color(222, 35, 130), edge_length=6)

    # Изменение цвета круга
    circle1.color = Color(55, 66, 77)
    print("Цвет круга:", circle1.color)

    # Попытка установить недопустимый цвет для куба
    try:
        cube1.color = Color(300, 70, 15)
    except ValueError as e:
        print("Ошибка:", e)
    print("Цвет куба:", cube1.color)

    # Попытка установить недопустимые стороны для куба
    try:
        cube1.sides = [5, 3, 12, 4, 5]
    except ValueError as e:
        print("Ошибка:", e)
    print("Стороны куба (должны иметь 12 одинаковых сторон):", cube1.get_sides())

    # Установка сторон для круга (хотя это не имеет смысла, так как круг имеет только одну сторону)
    circle1.sides = [15]
    print("Стороны круга:", circle1.sides)

    # Получение длины круга (сумма сторон)
    print("Длина окружности круга:", circle1.get_circumference())
    print("Общая длина всех сторон (в данном случае, длина окружности):", len(circle1))

    # Получение объема куба
    print("Объем куба:", cube1.get_volume())

    # Получение площади круга
    print("Площадь круга:", circle1.get_area())

    # Создание треугольника и получение его площади
    triangle1 = Triangle(3, 4, 5, Color(100, 150, 200))
    print("Площадь треугольника:", triangle1.get_area())

    # Получение информации о фигурах
    print("Информация о круге:", circle1.get_info())
    print("Информация о кубе:", cube1.get_info())
    print("Информация о треугольнике:", triangle1.get_info())
