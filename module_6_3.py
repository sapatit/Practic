import random


class Animal:
    def __init__(self, speed):
        self._cords = [0, 0, 0]
        self.speed = speed
        self.health = 100  # Начальное здоровье
        self.live = True
        self.sound = None
        self._DEGREE_OF_DANGER = 0

    def move(self, dx, dy, dz):
        new_z = self._cords[2] + dz * self.speed
        if new_z < 0:
            print("It's too deep, I can't dive :(")
        else:
            self._cords[0] += dx * self.speed
            self._cords[1] += dy * self.speed
            self._cords[2] = new_z

    def get_cords(self):
        print(f"Current position - X: {self._cords[0]}, Y: {self._cords[1]}, Z: {self._cords[2]}")

    def attack(self):
        if self._DEGREE_OF_DANGER < 5:
            print("Sorry, I'm peaceful :)")
        else:
            print("Be careful, I'm attacking you 0_0")

    def speak(self):
        print(self.sound)

    def find_food(self):
        food_found = random.choice([True, False])
        if food_found:
            print("Yay! I found some food!")
            return 10  # Возвращаем очки за нахождение пищи
        else:
            print("No food found, I'm still hungry.")
            self.health -= 10  # Уменьшаем здоровье
            if self.health <= 0:
                self.live = False
                print("Oh no! I'm too weak to continue.")
            return 0


class Bird(Animal):
    def lay_eggs(self):
        eggs = random.randint(1, 4)
        print(f"Here are(is) {eggs} eggs for you")


class AquaticAnimal(Animal):
    _DEGREE_OF_DANGER = 3

    def dive_in(self, dz):
        dz = abs(dz)
        dive_speed = self.speed / 2
        new_z = self._cords[2] - dz * dive_speed
        if new_z < 0:
            print("It's too deep, I can't dive :(")
        else:
            self._cords[2] = new_z


class PoisonousAnimal(Animal):
    _DEGREE_OF_DANGER = 8


class Duckbill(Bird, AquaticAnimal, PoisonousAnimal):
    sound = "Click-click-click"


class Enemy:
    def __init__(self, danger_level):
        self.danger_level = danger_level

    def attack(self, animal):
        print("An enemy attacks!")
        animal.health -= self.danger_level
        if animal.health <= 0:
            animal.live = False
            print("Oh no! You've been defeated!")


class Game:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.player = Duckbill(10)
        self.enemy = Enemy(danger_level=20)

    def add_score(self, points):
        self.score += points
        print(f"Score: {self.score}")
        self.check_level_up()

    def check_level_up(self):
        if self.score >= self.level * 100:  # Уровень повышается каждые 100 очков
            self.level += 1
            print(f"Congratulations! You've reached level {self.level}!")

    def check_health(self):
        print(f"Your health: {self.player.health}")

    def display_actions(self):
        print("\nChoose an action:")
        print("1. Move")
        print("2. Dive")
        print("3. Lay eggs")
        print("4. Find food")
        print("5. Encounter enemy")
        print("6. Check health")
        print("7. Quit")

    def game_loop(self):
        while self.player.live:  # Игра продолжается, пока игрок жив
            self.display_actions()
            action = input("Enter the number of your action: ").strip()
            if action == "1":
                dx = int(input("Enter dx: "))
                dy = int(input("Enter dy: "))
                dz = int(input("Enter dz: "))
                self.player.move(dx, dy, dz)
                self.player.get_cords()
            elif action == "2":
                dz = int(input("Enter dive depth: "))
                self.player.dive_in(dz)
                self.player.get_cords()
            elif action == "3":
                self.player.lay_eggs()
            elif action == "4":
                points = self.player.find_food()
                self.add_score(points)
            elif action == "5":
                self.enemy.attack(self.player)
                if not self.player.live:  # Проверяем, жив ли игрок после атаки
                    break
            elif action == "6":
                self.check_health()
            elif action == "7":
                print("Thanks for playing!")
                break
            else:
                print("Invalid action. Please enter a number from 1 to 7.")

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.game_loop()

