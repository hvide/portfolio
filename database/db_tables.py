# coding=utf-8

from database.base import Base
from sqlalchemy import Column, ForeignKey, Table, Integer, String, Float
from sqlalchemy.orm import relationship

# association_table = Table('association',
#                           Base.metadata,
#                           Column('fund_id', ForeignKey('funds.id')),
#                           Column('account_id', ForeignKey('accounts.id'))
#                           )


class Portfolio(Base):
    __tablename__ = 'portfolios'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True)

    accounts = relationship(
        'Account', back_populates='portfolio', cascade='all, delete')

    def __repr__(self) -> str:
        return f"<Portfolio {self.name}>"


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    value: Float = Column(Float)
    transaction_number = Column(Integer)

    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    portfolio = relationship('Portfolio', back_populates='accounts')

    account_types_id = Column(Integer, ForeignKey("account_types.id"))
    account_type = relationship('AccountType', back_populates='accounts')

    funds = relationship(
        'Fund', back_populates='account', cascade='all, delete')

    def __repr__(self) -> str:
        return f"<Account {self.id}>"


class AccountType(Base):
    __tablename__ = 'account_types'
    id = Column(Integer, primary_key=True)
    type = Column(String(30), nullable=False, unique=True)
    transaction_fee = Column(Float)
    annual_fee = Column(Float)

    accounts = relationship(
        'Account', back_populates='account_type', cascade='all, delete')

    def __repr__(self) -> str:
        return f"<AccountType {self.type}>"


class Fund(Base):
    __tablename__ = 'funds'

    id = Column(Integer, primary_key=True)
    weight = Column(Float, nullable=False)

    account_id = Column(Integer, ForeignKey("accounts.id"))
    account = relationship('Account', back_populates='funds')

    fund_types_id = Column(Integer, ForeignKey("fund_types.id"))
    fund_type = relationship('FundType', back_populates='funds')

    def __repr__(self) -> str:
        return f"<AccountType {self.fund_type}>"


class FundType(Base):
    __tablename__ = 'fund_types'

    id = Column(Integer, primary_key=True)
    isin = Column(String(12), nullable=False, unique=True)
    name = Column(String(200))
    nav = Column(Float)
    ofc = Column(Float)
    equity_pct = Column(Integer)
    url = Column(String(200))

    funds = relationship(
        'Fund', back_populates='fund_type', cascade='all, delete')

    def __repr__(self) -> str:
        return f"<Fund {self.isin}>"
