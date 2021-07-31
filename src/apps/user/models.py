from sqlalchemy import Column, String

from src.helpers.models import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    def __str__(self):
        return self.username
