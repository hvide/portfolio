# coding=utf-8

from sqlalchemy import Column, Float, String, Integer, Date

from database.base import Base


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), unique=False)
    transaction_fee = Column(Integer)
    annual_fee = Column(Float)

    def __init__(self, id, name, transaction_fee, annual_fee):
        self.id = id
        self.name = name
        self.transaction_fee = transaction_fee
        self.annual_fee = annual_fee

    def __repr__(self) -> str:
        return self.name
