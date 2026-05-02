import logging
import platform
import tomllib
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
APP_NAME: str = tomllib.load((BASE_DIR / 'pyproject.toml').open('rb'))['tool']['poetry']['name']
VERSION: str = tomllib.load((BASE_DIR / 'pyproject.toml').open('rb'))['tool']['poetry']['version']
PLATFORM: str = platform.platform()
IS_WINDOWS: bool = platform.system().lower() == 'windows'
ENV_FILE = BASE_DIR / ('env' if IS_WINDOWS else '.env')
RESTARTER_FILE: Path = BASE_DIR / 'reload_dir' / 'reload_log.txt'

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(ENV_FILE), env_file_encoding='utf-8')

    app_name: str = APP_NAME
    db: str = f'sqlite://{BASE_DIR / 'db.sqlite3'}'
    loglevel: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'INFO'
    log_to_file : bool = False
    log_stream: bool = False


settings = Settings()

logging_handlers = []
if settings.log_to_file:  # pragma: no cover
    logging_handlers.append(RotatingFileHandler(str(BASE_DIR / 'yerba.log'), maxBytes=5 * 1024 * 1024, backupCount=5))
if settings.log_stream:  # pragma: no cover
    logging_handlers.append(logging.StreamHandler())

logging.basicConfig(
    level=settings.loglevel,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=logging_handlers,
)


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
