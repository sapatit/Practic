import logging
from typing import Union

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class InputValidationError(Exception):
    """Исключение для ошибок валидации входных данных."""
    pass


class Team:
    """Класс, представляющий команду."""

    def __init__(self, name: str, participants: int, score: int, time: float) -> None:
        try:
            validate_input(participants, int)
            validate_input(score, int)
            validate_input(time, (int, float))
        except ValueError as e:
            raise InputValidationError(f"Ошибка валидации входных данных для команды '{name}': {e}")

        self.name: str = name
        self.participants: int = participants
        self.score: int = score
        self.time: float = time

    def get_participants_info(self) -> str:
        """Возвращает информацию о количестве участников команды."""
        return f"В команде {self.name} участников: {self.participants} !"

    def get_score_info(self) -> str:
        """Возвращает информацию о количестве решённых задач командой."""
        return f"Команда {self.name} решила задач: {self.score} !"

    def get_time_info(self) -> str:
        """Возвращает информацию о времени, затраченном на решение задач командой."""
        return f"{self.name} решила задачи за {self.time:.2f} с !"


class Competition:
    """Класс, представляющий соревнование между командами."""

    def __init__(self, team1: Team, team2: Team) -> None:
        self.teams = [team1, team2]

    def determine_winner(self) -> str:
        """Определяет победителя соревнования."""
        # Сравниваем команды по очкам и времени
        team1_score, team2_score = self.teams[0].score, self.teams[1].score
        team1_time, team2_time = self.teams[0].time, self.teams[1].time

        if team1_score > team2_score or (team1_score == team2_score and team1_time < team2_time):
            return f"Победа команды {self.teams[0].name}!"
        elif team1_score < team2_score or (team1_score == team2_score and team1_time > team2_time):
            return f"Победа команды {self.teams[1].name}!"
        else:
            return "Ничья!"

    def get_summary(self) -> str:
        """Возвращает сводку о соревновании."""
        return "\n".join([
                             team.get_participants_info() for team in self.teams
                         ] + [
                             team.get_score_info() for team in self.teams
                         ] + [
                             team.get_time_info() for team in self.teams
                         ] + [
                             self.determine_winner()
                         ])


def validate_input(value: Union[int, float], value_type: type) -> None:
    """Проверяет, соответствует ли значение ожидаемому типу."""
    if not isinstance(value, value_type):
        raise ValueError(f"Expected {value_type} but got {type(value)}")


def log_info(message: str) -> None:
    """Записывает информационное сообщение в лог."""
    logging.info(message)


def main() -> None:
    """Основная функция для выполнения программы."""
    try:
        # Входные данные
        team1: Team = Team("Мастера кода", 5, 40, 1552.512)
        team2: Team = Team("Волшебники данных", 6, 42, 2153.31451)

        # Создание соревнования
        competition: Competition = Competition(team1, team2)

        # Получение и вывод результатов
        summary: str = competition.get_summary()
        log_info(summary)
        print(summary)

        # Дополнительная информация
        tasks_total: int = 82
        time_avg: float = 45.2
        challenge_result: str = competition.determine_winner()

        # Вывод дополнительной информации
        additional_info: str = (
            f"Сегодня было решено {tasks_total} задач, в среднем по {time_avg} секунды на задачу!"
        )
        log_info(additional_info)
        print(additional_info)

    except InputValidationError as e:
        logging.error(f"Ошибка валидации входных данных: {e}")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()