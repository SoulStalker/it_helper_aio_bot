from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    boss_id: int


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env()

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
            boss_id=int(env('BOSS_ID'))
        ),
        db=DatabaseConfig(
            db_host=env('DB_HOST'),
            database=env('DB_URL'),
            db_user=env('DB_USER'),
            db_password=env('DB_PASSWORD')
        ),
    )

