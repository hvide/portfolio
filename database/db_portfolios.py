# coding=utf-8

# from database.funds import Fund
from database.base import Base
from sqlalchemy import Column, Float, ForeignKey, String, Integer
from sqlalchemy.orm import relationship


class Portfolio(Base):
    __tablename__ = 'portfolios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), unique=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))  # FK
    fund_isin = Column(String(16), ForeignKey('funds.isin'))  # FK
    transaction_number = Column(Integer)
    weight = Column(Float)

    fund = relationship('Fund', foreign_keys='Portfolio.fund_isin')
    account = relationship('Account', foreign_keys='Portfolio.account_id')

    def __init__(self, id, name, isin, transaction_number, weight):
        self.id = id
        self.name = name
        self.isin = isin
        self.transaction_number = transaction_number
        self.weight = weight

    def __repr__(self) -> str:
        return self.name
