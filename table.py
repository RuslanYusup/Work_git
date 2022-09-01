# импортируем необходимые объекты
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer

# инициализируем базу и установим наследование
Base = declarative_base()

class PprRawAll(Base):
    # установим название базы
    __tablename__ = "ppr_raw_all"
    # Создадим первичный численный ключ для id столбца
    id = Column(Integer, primary_key=True)