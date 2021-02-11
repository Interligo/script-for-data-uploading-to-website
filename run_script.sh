#!/bin/bash

echo 'Создаю виртуальное окружение.'
python -m venv venv

echo 'Активирую виртуальное окружение.'
source venv/Scripts/activate

echo 'Устанавливаю необходимые модули.'
python -m pip install -r requirements.txt

echo 'Начинаю подготовку к запуску скрипта.'
python ./main.py

echo 'Запускаю Джанго.'
python frontend/manage.py runserver
