import importlib
import types
from datetime import UTC, datetime

import config


def write_restart_log() -> None:
    with config.RESTARTER_FILE.open('a', encoding='utf-8') as f:
        date = datetime.now(tz=UTC).strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{date}: restarted \n')


async def perform_restart() -> None:
    write_restart_log()


def get_module(task_name: str) -> types.ModuleType|None:
    try:
        return importlib.import_module(f'tasks.{task_name}')
    except ModuleNotFoundError:
        pass
