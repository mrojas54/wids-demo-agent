#!/bin/bash

echo "Waiting for database to be ready..."

while ! nc -z web-db 5432; do
    sleep 0.1
done

echo "PostgreSQL started"

exec "$@"