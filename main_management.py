class MainManager:
    """
==========================================================================
Класс предназначен для взаимодействия с AirtableManager и DataBaseManager.
==========================================================================
Воспользуйтесь методом analyze_and_make_changes() и магия домашних эльфов всё сделает за Вас.
    """

    def __init__(self, airtable, database):
        self.airtable = airtable
        self.database = database

    def __str__(self):
        return f'Подключены: {self.airtable} и {self.database}'

    def __repr__(self):
        return f'Подключены: {self.airtable} и {self.database}'

    def _find_id_differences(self, id_from_db, id_from_airtable) -> list:
        """Функция для поиска новых ID, загруженных из Airtable."""
        if len(id_from_db) < len(id_from_airtable):
            difference = [id for id in id_from_airtable if id not in id_from_db]
        else:
            difference = [id for id in id_from_db if id not in id_from_airtable]
        return difference

    def _parse_json_by_id(self, psychotherapist_id) -> list:
        """Функция для поиска в json-файле данных о конкретном психотерапевте по ID."""
        data_to_add = []
        data_from_airtable = self.airtable.get_data()
        for element in data_from_airtable:
            if element['airtable_id'] == psychotherapist_id:
                data_to_add.append(element)
        return data_to_add

    def _data_conversion_to_list(self, data) -> list:
        """Функция для 'нормализации' данных о методах из БД в корректный для сравнения вид."""
        data = data.replace('{', '').replace('}', '')
        clean_data = data.split(',')
        return clean_data

    def _data_comparison(self, psychotherapist_id, data_from_db):
        """Функция для сверки свежих данных из Airtable и сохраненных в БД данных."""
        difference = {}
        data_from_json = self._parse_json_by_id(psychotherapist_id)
        methods_from_airtable = sorted(data_from_json[0]['methods'])
        methods_from_db = sorted(self._data_conversion_to_list(data_from_db.methods))
        if data_from_json[0]['name'] != data_from_db.name:
            difference['name'] = data_from_json[0]['name']
        if data_from_json[0]['photo'] != data_from_db.photo:
            difference['photo'] = data_from_json[0]['photo']
        if methods_from_airtable != methods_from_db:
            difference['methods'] = methods_from_airtable
        return difference

    def _make_changes(self):
        """Функция-агрегатор: перебирает ID и передает данные для сверки, если они различаются, то вносит изменения."""
        id_from_airtable = self.airtable.get_id()
        for psychotherapist_id in id_from_airtable:
            data_from_db = self.database.get_data_by_id(psychotherapist_id)
            data_to_update = self._data_comparison(psychotherapist_id, data_from_db)
            if data_to_update:
                self._update_psychotherapist_data(psychotherapist_id, data_to_update)
                print('Обнаружены обновленные данные. Вношу изменения в базу данных.')

    def _add_new_psychotherapist(self, psychotherapist_id):
        """Функция для сохранения новых данных в БД."""
        data_to_add = self._parse_json_by_id(psychotherapist_id)
        airtable_id = data_to_add[0]['airtable_id']
        name = data_to_add[0]['name']
        photo = data_to_add[0]['photo']
        methods = data_to_add[0]['methods']
        self.database.save_psychotherapist_data_to_db(airtable_id, name, photo, methods)

    def _update_psychotherapist_data(self, psychotherapist_id, data_to_update):
        """Функция для обновления данных в БД."""
        self.database.update_psychotherapist_data_in_db(psychotherapist_id, data_to_update)

    def _delete_psychotherapist(self, psychotherapist_id):
        """Функция для удаления данных из БД."""
        self.database.delete_psychotherapist_data_from_db(psychotherapist_id)

    def analyze_and_make_changes(self):
        """Функция-агрегатор: запускает цикл анализа данных из Airtable и сравнения с данными из БД."""
        self.database._create_table_if_not_exist('psychotherapist')
        id_from_db = self.database.get_id()
        id_from_airtable = self.airtable.get_id()

        if id_from_db != id_from_airtable:
            different_ids = self._find_id_differences(id_from_db, id_from_airtable)

            if len(id_from_db) < len(id_from_airtable):  # Create
                for psychotherapist_id in different_ids:
                    self._add_new_psychotherapist(psychotherapist_id)
                    print('Обнаружены новые данные. Загружаю в базу данных.')

            elif len(id_from_db) > len(id_from_airtable):  # Delete
                for psychotherapist_id in different_ids:
                    self._delete_psychotherapist(psychotherapist_id)
                    print('Обнаружены устаревшие данные. Удаляю их из базы данных.')

        elif id_from_db == id_from_airtable:  # Update
            print('Новых или устаревших данных не обнаружено.')
            self._make_changes()
