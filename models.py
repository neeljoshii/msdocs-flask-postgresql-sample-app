from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import validates

from app import db


class Products(db.Model):
    __tablename__ = 'Products'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(db.Float)
