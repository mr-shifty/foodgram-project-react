#!/bin/bash

# Запуск миграций
python manage.py migrate

# Импорт ингредиентов
python manage.py import_csv

# Сборка статики
python manage.py collectstatic

# Запуск сервера
exec "$@"