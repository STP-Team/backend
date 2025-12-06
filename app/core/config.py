from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    API_HOST: str
    API_PORT: int

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    def construct_sqlalchemy_url(
        self,
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
            username=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT if self.DB_PORT else 3306,
            database=self.DB_NAME,
            query={
                "charset": "utf8mb4",
                "use_unicode": "1",
                "sql_mode": "TRADITIONAL",
                "connect_timeout": "30",
                "autocommit": "false",
            },
        )

        return connection_url


settings = Settings()
