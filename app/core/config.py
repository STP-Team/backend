from dataclasses import dataclass

from environs import Env
from sqlalchemy import URL


@dataclass
class APIConfig:
    port: int
    jwt_secret_key: str

    @staticmethod
    def from_env(env: Env):
        """Создает объект DbConfig из переменных окружения.

        Args:
            env: Объект переменных окружения

        Returns:
            Собранный объект DbConfig
        """
        port = env.int("API_PORT")
        jwt_secret_key = env.str("JWT_SECRET_KEY")

        return APIConfig(
            port=port,
            jwt_secret_key=jwt_secret_key,
        )


@dataclass
class DbConfig:
    """Класс конфигурации подключения к базам данных.

    Attributes:
        host: Адрес сервера
        user: Логин пользователя БД
        password: Пароль пользователя БД

        db_name: Название базы данных
    """

    host: str
    user: str
    password: str
    db_name: str

    def construct_sqlalchemy_url(
        self,
        db_name=None,
        driver="aiomysql",
    ) -> URL:
        """Собирает строку SQLAlchemy для подключения к MariaDB.

        Args:
            db_name: Название базы данных
            driver: Драйвер для подключения

        Returns:
            Возвращает собранную строку для подключения к базе используя SQLAlchemy
        """
        connection_url = URL.create(
            f"mysql+{driver}",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port if hasattr(self, "port") and self.port else 3306,
            database=db_name,
            query={
                "charset": "utf8mb4",
                "use_unicode": "1",
                "sql_mode": "TRADITIONAL",
                "connect_timeout": "30",
                "autocommit": "false",
            },
        )

        return connection_url

    @staticmethod
    def from_env(env: Env):
        """Создает объект DbConfig из переменных окружения.

        Args:
            env: Объект переменных окружения

        Returns:
            Собранный объект DbConfig
        """
        host = env.str("DB_HOST")
        user = env.str("DB_USER")
        password = env.str("DB_PASS")
        db_name = env.str("DB_NAME")

        return DbConfig(
            host=host,
            user=user,
            password=password,
            db_name=db_name,
        )


@dataclass
class Config:
    """Основной класс конфигурации.

    Этот класс содержит все остальные классы конфигурации, предоставляя централизованный доступ ко всем настройкам.

    Attributes:
    ----------
    api: Содержит настройки API сервера
    db: Содержит настройки подключения к базе данных
    """

    api: APIConfig
    db: DbConfig


def load_config(path: str = None) -> Config:
    """Загружает конфиг из переменных окружения.

    Читает либо значения из файла .env, если предоставлен путь до него, иначе читает из переменных запущенного процесса.
    Если path не указан, пытается найти .env файл в стандартных местах.

    Args:
        path: Опциональный путь к файлу переменных окружения

    Returns:
        Объект Config с аттрибутами для каждого класса конфигурации
    """
    env = Env()
    env.read_env(path)

    return Config(
        api=APIConfig.from_env(env),
        db=DbConfig.from_env(env),
    )
