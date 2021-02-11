import os
import json
from airtable import Airtable
from requests import HTTPError

from load_env import load_env


load_env()


class AirtableManager:
    """
=================================================
Класс предназначен для взаимодействия с Airtable.
=================================================
Воспользуйтесь методом save_data() для выгрузки информации из таблицы.
Воспользуйтесь методом read_data() для ознакомления с выгруженной информацией.
Воспользуйтесь методом get_id() для получения ID психотерапевтов.
Воспользуйтесь методом get_unique_methods() для получения списка методов психотерапевтов в таблице.
    """

    def __init__(self):
        self.api_key = os.getenv('PERSONAL_API_KEY')
        self.base_id = os.getenv('BASE_ID')
        self.table_name = os.getenv('TABLE_NAME')
        self.file_to_save_data = 'airtable_data.json'

    def __str__(self):
        return f'Подключена таблица {self.table_name}'

    def __repr__(self):
        return f'Таблица {self.table_name}'

    def _get_connection(self):
        """Возвращает подключение к Airtable."""
        connection = Airtable(self.base_id, self.table_name, self.api_key)
        return connection

    def _get_data(self):
        """Подключается к Airtable и получает данные."""
        airtable = self._get_connection()
        try:
            data_from_airtable = airtable.get_all()
            return data_from_airtable
        except HTTPError:
            raise SystemExit('Не удалось подключиться к Airtable.')

    def _parse_data(self):
        """Возвращает список психотерапевтов с необходимой информацией."""
        parsed_data = []
        data_from_airtable = self._get_data()
        for element in data_from_airtable:
            airtable_id = element['id']
            name = element['fields']['Имя']
            methods = element['fields']['Методы']
            photo = element['fields']['Фотография'][0]['url']
            payload = {'airtable_id': airtable_id, 'name': name, 'methods': methods, 'photo': photo}
            parsed_data.append(payload)
        return parsed_data

    def save_raw_data(self):
        """Сохраняет все данные в json-файл."""
        data = self._get_data()
        file_name = 'raw_' + self.file_to_save_data
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, sort_keys=True, indent=4, ensure_ascii=False)

    def save_data(self):
        """Сохраняет необходимые данные в json-файл."""
        data = self._parse_data()
        with open(self.file_to_save_data, 'w', encoding='utf-8') as file:
            json.dump(data, file, sort_keys=True, indent=4, ensure_ascii=False)

    def get_raw_data(self):
        """Получает данные из json-файла. Если его не существует, то вызывает метод save_raw_data()."""
        file_name = 'raw_' + self.file_to_save_data
        if not os.path.exists(file_name):
            self.save_raw_data()
        with open(file_name, 'r', encoding='utf-8') as file:
            loaded_data = json.load(file)
        return loaded_data

    def get_data(self):
        """Получает данные из json-файла. Если его не существует, то вызывает метод save_data()."""
        if not os.path.exists(self.file_to_save_data):
            self.save_data()
        with open(self.file_to_save_data, 'r', encoding='utf-8') as file:
            loaded_data = json.load(file)
        return loaded_data

    def get_id(self) -> tuple:
        """Возвращает список id психотерапевтов."""
        all_airtable_id = []
        data_from_json = self.get_data()
        for element in data_from_json:
            all_airtable_id.append(element['airtable_id'])
        all_airtable_id = tuple(all_airtable_id)
        return all_airtable_id

    def get_unique_methods(self) -> list:
        """Возвращает список уникальных методов для всех психотерапевтов."""
        all_methods = []
        data_from_json = self.get_data()
        for element in data_from_json:
            for method in element['methods']:
                all_methods.append(method)
        unique_methods = list(set(all_methods))
        return unique_methods
