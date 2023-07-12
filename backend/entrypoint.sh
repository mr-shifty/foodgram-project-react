#!/bin/bash

# Запуск миграций
python manage.py migrate && python manage.py import_csv

# Сборка статики
python manage.py collectstatic

# Копирование статики в папку с контейнером nginx
cp -r /app/collected_static/. /kittygram_backend_static/static/

# Запуск сервера
exec "$@"