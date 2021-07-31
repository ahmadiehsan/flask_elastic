from sqlalchemy import Column, Integer, DateTime, func

from src.db import SQLAlchemyBase


class BaseModel(SQLAlchemyBase):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime, default=func.now())
    update_time = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<{self.__class__.__name__.lower()} {self.id}>'
