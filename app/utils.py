from datetime import UTC, datetime

from config import settings


async def perform_restart() -> None:
    with settings.restarter_file.open('a', encoding='utf-8') as f:
        date = datetime.now(tz=UTC).strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{date}: restarted \n')
