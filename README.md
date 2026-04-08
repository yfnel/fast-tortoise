# FastAPI Tortoise ORM pytest working example 

## installation
* `poetry install --with utils`

## dev server
* `uvicorn main:app --reload`


## tests
* `py.test -s --cov . --cov-report=term-missing --cov-fail-under=100 --no-cov-on-fail --tb long`
* `ruff check . && ruff check --select E301,E305,E303,E501 --preview .`

