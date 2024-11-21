import hashlib
import time
import secrets
import logging
from dataclasses import dataclass, field
from typing import List, Optional, Dict

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class User:
    nickname: str
    password: str
    age: int
    comments: List[str] = field(default_factory=list)
    history: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.password = self.hash_password(self.password)

    @staticmethod
    def hash_password(password: str) -> str:
        salt: str = secrets.token_hex(16)
        hashed: str = hashlib.sha256((salt + password).encode()).hexdigest()
        return f"{salt}${hashed}"

    def check_password(self, password: str) -> bool:
        salt, hashed = self.password.split('$')
        return hashed == hashlib.sha256((salt + password).encode()).hexdigest()

    def __str__(self):
        return f"User(nickname={self.nickname}, age={self.age})"


@dataclass
class Video:
    title: str
    duration: int
    current_time: int = 0
    adult_mode: bool = False
    comments: List[str] = field(default_factory=list)

    def add_comment(self, comment: str) -> None:
        self.comments.append(comment)

    def __str__(self):
        return f"Video(title={self.title}, duration={self.duration}, adult_mode={self.adult_mode})"


class UrTube:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.videos: Dict[str, Video] = {}
        self.current_user: Optional[User] = None

    def log_in(self, nickname: str, password: str) -> None:
        user = self.users.get(nickname)
        if user and user.check_password(password):
            self.current_user = user
            logging.info(f"Пользователь {nickname} вошел в систему.")
        else:
            logging.warning("Неверный логин или пароль")

    def register(self, nickname: str, password: str, age: int) -> None:
        if nickname in self.users:
            logging.warning(f"Пользователь {nickname} уже существует")
            return
        self.users[nickname] = User(nickname, password, age)
        self.current_user = self.users[nickname]
        logging.info(f"Пользователь {nickname} зарегистрирован.")

    def log_out(self) -> None:
        if self.current_user:
            logging.info(f"Пользователь {self.current_user.nickname} вышел из системы.")
        self.current_user = None

    def add(self, *videos: Video) -> None:
        for video in videos:
            if video.title not in self.videos:
                self.videos[video.title] = video
                logging.info(f"Видео '{video.title}' добавлено.")

    def get_videos(self, keyword: str) -> List[str]:
        return [video.title for video in self.videos.values() if keyword.lower() in video.title.lower()]

    def watch_video(self, title: str) -> None:
        if self.current_user is None:
            logging.warning("Попытка просмотра видео без входа в аккаунт.")
            raise PermissionError("Войдите в аккаунт, чтобы смотреть видео")

        video = self.videos.get(title)
        if video is None:
            logging.warning(f"Видео '{title}' не найдено.")
            raise ValueError("Видео не найдено")

        if video.adult_mode and self.current_user.age < 18:
            logging.warning(f"Пользователь {self.current_user.nickname} не может смотреть видео '{title}' из-за возрастного ограничения.")
            raise PermissionError("Вам нет 18 лет, пожалуйста, покиньте страницу")

        for second in range(1, video.duration + 1):
            print(second, end=' ', flush=True)
            time.sleep(1)  # Имитация воспроизведения видео
        print("Конец видео")
        self.current_user.history.append(video.title)
        logging.info(f"Пользователь {self.current_user.nickname} посмотрел видео '{title}'.")

    def add_comment(self, video_title: str, comment: str) -> None:
        video = self.videos.get(video_title)
        if video:
            video.add_comment(comment)
            logging.info(f"Пользователь {self.current_user.nickname} добавил комментарий к видео '{video_title}': {comment}")
            print(f"Комментарий добавлен к видео '{video_title}'")
        else:
            logging.warning(f"Попытка добавления комментария к несуществующему видео '{video_title}'.")
            raise ValueError("Видео не найдено")

    def display_comments(self, video_title: str) -> None:
        video = self.videos.get(video_title)
        if video:
            comments = video.comments
            if comments:
                print(f"Комментарии к видео '{video_title}':")
                for comment in comments:
                    print(f"- {comment}")
                logging.info(f"Вывод комментариев для видео '{video_title}'.")
            else:
                print(f"Нет комментариев к видео '{video_title}'")
                logging.info(f"Нет комментариев для видео '{video_title}'.")
        else:
            logging.warning(f"Попытка вывода комментариев для несуществующего видео '{video_title}'.")
            raise ValueError("Видео не найдено")

    def get_watch_history(self) -> List[str]:
        if self.current_user:
            return self.current_user.history
        else:
            raise PermissionError("Войдите в аккаунт, чтобы просмотреть историю")

    def get_comments(self, video_title: str) -> List[str]:
        video = self.videos.get(video_title)
        if video:
            return video.comments
        else:
            raise ValueError("Видео не найдено")


# Пример использования
if __name__ == "__main__":
    ur = UrTube()

    v1 = Video('Лучший язык программирования 2024 года', 200)
    v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

    # Добавление видео
    ur.add(v1, v2)

    # Проверка поиска
    print(ur.get_videos('лучший'))  # ['Лучший язык программирования 2024 года']
    print(ur.get_videos('ПРОГ'))     # ['Лучший язык программирования 2024 года', 'Для чего девушкам парень программист?']

    # Проверка на вход пользователя и возрастное ограничение
    try:
        ur.watch_video('Для чего девушкам парень программист?')  # Войдите в аккаунт, чтобы смотреть видео
    except PermissionError as e:
        print(e)

    # Регистрация пользователей
    ur.register('vasya_pupkin', 'lolkekcheburek', 13)
    try:
        ur.watch_video('Для чего девушкам парень программист?')  # Вам нет 18 лет, пожалуйста покиньте страницу
    except PermissionError as e:
        print(e)

    ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
    try:
        ur.watch_video('Для чего девушкам парень программист?')  # Воспроизведение видео
    except Exception as e:
        print(e)

    # Проверка входа в другой аккаунт
    ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)  # Пользователь vasya_pupkin уже существует
    print(ur.current_user)  # urban_pythonist

    # Попытка воспроизведения несуществующего видео
    try:
        ur.watch_video('Лучший язык программирования 2024 года!')  # Видео не найдено
    except ValueError as e:
        print(e)

    # Добавление комментариев к видео
    try:
        ur.add_comment('Лучший язык программирования 2024 года', 'Отличное видео! Очень информативно.')
        ur.add_comment('Для чего девушкам парень программист?', 'Согласен, программисты - лучшие!')
    except ValueError as e:
        print(e)

    # Вывод комментариев для проверки
    try:
        ur.display_comments('Лучший язык программирования 2024 года')
        ur.display_comments('Для чего девушкам парень программист?')
    except ValueError as e:
        print(e)

    # Получение истории просмотров
    try:
        history = ur.get_watch_history()
        print("История просмотров:", history)
    except PermissionError as e:
        print(e)

    # Получение комментариев к видео
    try:
        comments_for_video_1 = ur.get_comments('Лучший язык программирования 2024 года')
        print("Комментарии к видео 'Лучший язык программирования 2024 года':", comments_for_video_1)

        comments_for_video_2 = ur.get_comments('Для чего девушкам парень программист?')
        print("Комментарии к видео 'Для чего девушкам парень программист?':", comments_for_video_2)
    except ValueError as e:
        print(e)