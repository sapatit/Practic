import threading
import time
import logging
import json
import sys
import argparse


class Enemy:
    def __init__(self, total_enemies):
        self.total_enemies = total_enemies

    def reduce_enemies(self, power):
        self.total_enemies -= power
        return max(self.total_enemies, 0)


class Knight(threading.Thread):
    lock = threading.Lock()  # Мьютекс для синхронизации доступа к общему ресурсу

    def __init__(self, name, power, enemy):
        super().__init__()
        self.name = name
        self.power = power
        self.days = 0
        self.enemy = enemy

    def run(self):
        logging.info(f"{self.name}, на нас напали!")
        self.battle()

    def battle(self):
        while True:
            with Knight.lock:  # Защита доступа к общему ресурсу
                if self.enemy.total_enemies <= 0:
                    break
                remaining_enemies = self.enemy.reduce_enemies(self.power)
                self.days += 1
                self.report_status(remaining_enemies)

            time.sleep(1)  # Задержка в 1 секунду

        logging.info(f"{self.name} одержал победу спустя {self.days} дней(дня)!")

    def report_status(self, remaining_enemies):
        logging.info(f"{self.name}, сражается {self.days} день(дня)..., осталось {remaining_enemies} воинов.")


def load_config(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Knight Battle Simulation")
    parser.add_argument('config_file', type=str, help='Path to the configuration file')
    parser.add_argument('--log_level', type=str, default='INFO',
                        help='Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
    return parser.parse_args()


def main():
    args = parse_arguments()

    # Настройка уровня логирования
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO))

    config = load_config(args.config_file)
    enemy = Enemy(config['total_enemies'])

    knights = []
    for knight_data in config['knights']:
        knight = Knight(knight_data['name'], knight_data['power'], enemy)
        knights.append(knight)

    # Запуск потоков
    for knight in knights:
        knight.start()

    # Ожидание завершения потоков
    for knight in knights:
        knight.join()

    # Вывод строки об окончании сражения
    logging.info("Все битвы закончились!")


if __name__ == "__main__":
    main()
