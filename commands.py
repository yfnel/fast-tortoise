
import typer

from app.utils import write_restart_log

app = typer.Typer()


@app.command()
def restart() -> None:
    write_restart_log()


if __name__ == '__main__':
    app()
