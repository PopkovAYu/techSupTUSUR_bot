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

# Creating examplair of Env class
env: Env = Env()

# Adding data from .env to enviroment variables
env.read_env()

# Creating Config class examplair and fill it with data from env var
config = Config(
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

print('BOT_TOKEN:', config.tg_bot.token)
print('ADMIN_IDS:', config.tg_bot.admin_ids)
print()
print('DATAABASE:', config.db.database)
print('DB_HOST:', config.db.db_host)
print('DB_USER:', config.db.db_user)
print('DB_PASSWORD:', config.db.db_password)