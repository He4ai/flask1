import datetime
import os
import atexit
from sqlalchemy import create_engine, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, MappedColumn, mapped_column

POSTGRES_USER = os.getenv("POSTGRES_USER", 'postgres')
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", 'root')
POSTGRES_HOST = os.getenv("POSTGRES_HOST", '127.0.0.1')
POSTGRES_DB = os.getenv("POSTGRES_DB", 'flask_pr')
POSTGRES_PORT = os.getenv("POSTGRES_PORT", '5431')

PG_DSN = (f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class Ann(Base):
    __tablename__ = "announcements"

    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    title: MappedColumn[str] = mapped_column(String, nullable=False)
    descr: MappedColumn[str] = mapped_column(String, nullable=False)
    creation_date: MappedColumn[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner: MappedColumn[str] = mapped_column(String, nullable=False)

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "descr": self.descr,
            "creation_date": self.creation_date.isoformat(),
            "owner": self.owner
        }

Base.metadata.create_all(engine)
atexit.register(engine.dispose)
