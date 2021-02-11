#!/usr/bin/env python

from airtable_management import AirtableManager
from db_management import DataBaseManager
from main_management import MainManager


# TODO: SLI скрипт, добавить запуск через exe
# TODO: Дополнить main развертываением сайта

def main():
    print('Скрипт запускается...')
    airtable = AirtableManager()
    database = DataBaseManager()
    manager = MainManager(airtable, database)
    print('Инициализация завершена.')

    # Сохранение сырых данных из Airtable в базу данных при каждом запуске скрипта
    airtable.save_raw_data()
    raw_data = airtable.get_raw_data()
    database.save_raw_data_to_db(raw_data)
    print('Бэкап загружен в базу данных.')

    # Сохранение только необходимых данных из Airtable
    airtable.save_data()
    print('Приступаю к анализу данных...')

    # Анализ данных и внесение изменений, при необходимости
    manager.analyze_and_make_changes()
    print('Работа скрипта завершена.')


if __name__ == '__main__':
    main()
