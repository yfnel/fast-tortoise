import platform
import tomllib
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    app_name: str = 'Fast-Tortoise'
    version: str = tomllib.load((BASE_DIR / 'pyproject.toml').open('rb'))['tool']['poetry']['version']
    platform: str = platform.platform()
    db: str = f'sqlite://{BASE_DIR / 'db.sqlite3'}'
    base_dir: Path = BASE_DIR
    restarter_file: Path = BASE_DIR / 'restart_log.txt'


settings = Settings()


TORTOISE_ORM = {
    'connections': {
        'default': settings.db,
    },
    'apps': {
        'models': {
            'models': ['app.models'],
            'default_connection': 'default',
            'migrations': 'app.migrations',
        },
    },
    'use_tz': True,
    'timezone': 'UTC',
}
