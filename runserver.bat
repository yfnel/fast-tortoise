@echo off
setlocal

IF NOT DEFINED UVICORN_HOST SET "UVICORN_HOST=localhost"
IF NOT DEFINED UVICORN_PORT SET "UVICORN_PORT=8000"


cd /d "%~dp0"
"%~dp0\.venv\Scripts\python.exe" -m uvicorn app.main:app --host %UVICORN_HOST% --port %UVICORN_PORT% --reload --reload-dir "reload_dir" --reload-include "reload_log.txt"
