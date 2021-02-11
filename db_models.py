import datetime
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import TIMESTAMP
from sqlalchemy import JSON
from sqlalchemy import VARCHAR
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel(Base):
    """Базовая модель для базы данных."""
    __abstract__ = True
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)

    def __str__(self):
        return f'Экземпляр класса {__class__.__name__}'

    def __repr__(self):
        return __class__.__name__


class Psychotherapist(BaseModel):
    """Модель психотерапевта для создания таблицы в базе данных."""
    __tablename__ = 'psychotherapist'
    airtable_id = Column(VARCHAR(50), nullable=False)
    name = Column(VARCHAR(100), nullable=False)
    photo = Column(VARCHAR(100), nullable=True)
    methods = Column(VARCHAR(150), nullable=True)

    def __init__(self, airtable_id, name, photo, methods):
        self.airtable_id = airtable_id
        self.name = name
        self.photo = photo
        self.methods = methods

    def __str__(self):
        return f'airtable_id: {self.airtable_id}, name: {self.name}, photo: {self.photo}, methods: {self.methods}'

    def __repr__(self):
        return f'airtable_id: {self.airtable_id}, name: {self.name}, photo: {self.photo}, methods: {self.methods}'


class PsychotherapistRawData(BaseModel):
    """Модель для таблицы с сырыми данными в базе."""
    __tablename__ = 'psychotherapist_raw_data'
    data = Column(JSON, nullable=False)
    creation_time = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now)

    def __init__(self, data, creation_time):
        self.data = data
        self.creation_time = creation_time

    def __str__(self):
        return f'Данные от {self.creation_time}: {self.data}'

    def __repr__(self):
        return f'Данные от {self.creation_time}: {self.data}'
