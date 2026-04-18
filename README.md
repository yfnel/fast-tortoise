# FastAPI Tortoise ORM pytest working example 

## installation
* `poetry install --with utils`

## OCR
* `sudo apt install tesseract-ocr`
* `sudo apt install tesseract-ocr-pol`

## dev server
* `uvicorn app.main:app --reload`

## server with remote reload
* `uvicorn  app.main:app --reload --reload-include 'restart_log.txt'`

## tests
* `py.test -s --cov . --cov-report=term-missing --cov-fail-under=100 --no-cov-on-fail --tb long`
* `ruff check . && ruff check --select E301,E305,E303,E501 --preview .`
