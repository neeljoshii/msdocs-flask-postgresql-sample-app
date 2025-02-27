from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import validates

from app import db


class Products(db.Model):
    __tablename__ = 'Products'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = db.Column(db.Text)
    price = Column(db.Float)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
