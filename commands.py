import typer

from app.utils import get_module, write_restart_log

app = typer.Typer()


@app.command()
def restart() -> None:
    write_restart_log()
    typer.secho('DONE', fg='green')


@app.command(context_settings={'allow_extra_args': True, 'ignore_unknown_options': True})
def run_task(task_name: str, ctx: typer.Context=None) -> None:
    task = get_module(task_name)
    args = ctx.args if ctx else []
    typer.secho(f'STARTING {task_name}', fg='green')
    task.run(*args)


if __name__ == '__main__':  # pragma: no cover
    app()
