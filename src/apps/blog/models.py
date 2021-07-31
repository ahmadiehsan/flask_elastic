from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import backref, relationship

from src.helpers.models import BaseModel


class Post(BaseModel):
    __tablename__ = 'post'

    title = Column(String(80), nullable=False)
    content = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship('Category', backref=backref('posts', lazy=True))

    def __str__(self):
        return self.title


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name
