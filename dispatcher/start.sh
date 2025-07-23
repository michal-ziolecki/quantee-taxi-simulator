#!/bin/sh
# run migrations
export ALEMBIC_CONFIG=db/alembic.ini
alembic upgrade head
# run api
#uvicorn start:app --host 0.0.0.0 --port 8080 --timeout-keep-alive 10 --timeout-graceful-shutdown 60 --workers 4 --log-level info
# for development
uvicorn start:app --host 0.0.0.0 --port 8080 --workers 1 --log-level debug --reload
