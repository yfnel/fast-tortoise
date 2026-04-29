# FastAPI Tortoise ORM pytest working example 

## installation
* `poetry install --with utils`

## installation - windows
* `python.exe -m poetry config virtualenvs.in-project true`
* `python.exe -m poetry config virtualenvs.use-poetry-python true`
* `python.exe -m poetry install --with utils --with windows`

## dev server
* `uvicorn app.main:app --reload`

## server with remote reload
* `uvicorn app.main:app --reload --reload-dir 'reload_dir' --reload-include 'reload_log.txt'`

## tests
* `py.test -s --cov . --cov-report=term-missing --cov-fail-under=100 --no-cov-on-fail --tb long`
* `ruff check . && ruff check --select E301,E305,E303,E501 --preview .`
