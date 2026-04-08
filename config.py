import subprocess
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
VERSION = subprocess.run(['poetry', 'version'], check=False, capture_output=True, text=True).stdout.strip()  # noqa: S607


class Settings(BaseSettings):
    app_name: str = 'Fast-Tortoise'
    version: str = VERSION
    db: str = 'sqlite://db.sqlite3'
    base_dir: Path = BASE_DIR


settings = Settings()


TORTOISE_ORM = {
    'connections': {
        'default': settings.db,
    },
    'apps': {
        'models': {
            'models': ['models'],
            'default_connection': 'default',
            'migrations': 'migrations',
        },
    },
    'use_tz': True,
    'timezone': 'UTC',
}
