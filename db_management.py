import os
import datetime
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from load_env import load_env
from db_models import Base
from db_models import Psychotherapist
from db_models import PsychotherapistRawData


load_env()


def data_conversion_to_tuple(data: list) -> tuple:
    """Функция для преобразования данных в удобочитемый вид."""
    result = []
    for element in data:
        result.append(*element)
    result = tuple(result)
    return result


class DataBaseManager:
    """
================================================================
Класс предназначен для взаимодействия с базой данных PostgreSQL.
================================================================
Воспользуйтесь методом add_psychotherapist() для загрузки информации в таблицу.
Воспользуйтесь методом get_data() для ознакомления с выгруженной информацией.
Воспользуйтесь методом get_id() для получения ID психотерапевтов из базы данных.
Воспользуйтесь методом get_data_by_id() для получения данных по ID психотерапевта.
    """

    def __init__(self):
        self.user = os.getenv('DATABASE_USER')
        self.password = os.getenv('DATABASE_PASSWORD')
        self.host = os.getenv('DATABASE_HOST')
        self.port = os.getenv('DATABASE_PORT')
        self.database_name = os.getenv('DATABASE_NAME')

    def __str__(self):
        return f'База данных: {self.database_name}'

    def __repr__(self):
        return f'База данных: {self.database_name}'

    def _get_connection(self):
        """Возвращает подключение к PostgreSQL."""
        engine = create_engine(f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database_name}',
                               pool_pre_ping=True)
        return engine

    def _create_session(self):
        """Создает сессию для взаимодействия с базой данных."""
        engine = self._get_connection()
        db_session = sessionmaker(engine)
        session = db_session()
        return session

    def _create_table_if_not_exist(self, table_name):
        """Создает таблицу если её не существует."""
        engine = self._get_connection()
        try:
            if not engine.dialect.has_table(engine, table_name):
                Base.metadata.create_all(engine, tables=[Base.metadata.tables[table_name]])
        except OperationalError:
            raise SystemExit('Не удалось подключиться к PostgreSQL.')

    def save_raw_data_to_db(self, data):
        """Добавляет данные в таблицу Psychotherapist_raw_data."""
        self._create_table_if_not_exist('psychotherapist_raw_data')
        session = self._create_session()
        raw_data = PsychotherapistRawData(data=data, creation_time=datetime.datetime.now())
        session.add(raw_data)
        return session.commit()

    def save_psychotherapist_data_to_db(self, airtable_id, name, photo, methods):
        """Добавляет данные в таблицу Psychotherapist."""
        self._create_table_if_not_exist('psychotherapist')
        session = self._create_session()
        new_psychotherapist = Psychotherapist(airtable_id=airtable_id, name=name, photo=photo, methods=methods)
        session.add(new_psychotherapist)
        return session.commit()

    def update_psychotherapist_data_in_db(self, airtable_id, data_to_update):
        """Обновляет данные из таблицы Psychotherapist."""
        self._create_table_if_not_exist('psychotherapist')
        session = self._create_session()
        session.query(Psychotherapist).filter(Psychotherapist.airtable_id == airtable_id).update(data_to_update)
        return session.commit()

    def delete_psychotherapist_data_from_db(self, airtable_id):
        """Удаляет данные из таблицы Psychotherapist."""
        self._create_table_if_not_exist('psychotherapist')
        session = self._create_session()
        psychotherapist_to_delete = session.query(Psychotherapist).filter_by(airtable_id=airtable_id).first()
        session.delete(psychotherapist_to_delete)
        return session.commit()

    def get_data(self):
        """Выгружает все данные из таблицы Psychotherapist."""
        session = self._create_session()
        psychotherapists = session.query(Psychotherapist).all()
        return psychotherapists

    def get_raw_data(self):
        """Выгружает все данные из таблицы Psychotherapist raw data."""
        session = self._create_session()
        raw_data = session.query(PsychotherapistRawData).all()
        return raw_data

    def get_data_by_id(self, airtable_id):
        """Выгружает данные по ID из таблицы Psychotherapist."""
        session = self._create_session()
        psychotherapists = session.query(Psychotherapist).filter_by(airtable_id=airtable_id).first()
        return psychotherapists

    def get_id(self):
        """Выгружает только ID из таблицы Psychotherapist."""
        session = self._create_session()
        psychotherapists_id = session.query(Psychotherapist.airtable_id).all()
        data = data_conversion_to_tuple(psychotherapists_id)
        return data
