import platform
import tomllib
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent
VERSION: str = tomllib.load((BASE_DIR / 'pyproject.toml').open('rb'))['tool']['poetry']['version']
PLATFORM: str = platform.platform()

class Settings(BaseSettings):
    app_name: str = 'Fast-Tortoise'
    db: str = f'sqlite://{BASE_DIR / 'db.sqlite3'}'
    restarter_file: Path = BASE_DIR / 'reload_dir' / 'reload_log.txt'


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
