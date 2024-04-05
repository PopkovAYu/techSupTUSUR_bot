from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str  # database name
    db_host: str  # DB URL
    db_user: str  # DB user's Username
    db_password: str  # DB password


@dataclass
class TgBot:
    token: str  # bot token
    admin_ids: list[int]  # admin ids list


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config(path: str | None = None) -> Config:

    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        ),
        db=DatabaseConfig(
            database=env('DATABASE'),
            db_host=env('DB_HOST'),
            db_user=env('DB_USER'),
            db_password=env('DB_PASSWORD')
        )
    )
