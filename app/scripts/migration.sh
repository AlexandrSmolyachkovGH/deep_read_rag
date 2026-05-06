#!/bin/sh

echo "WAIT FOR PG HEALTHY STATUS"

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT_INNER; do
  sleep 2
done

echo "PG IS HEALTHY"

echo "START DB MIGRATIONS"
poetry run alembic upgrade head
echo "FINISH DB MIGRATIONS"

echo "START API"
exec poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
