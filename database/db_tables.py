# coding=utf-8

from database.base import Base
from sqlalchemy import Column, ForeignKey, Table, Integer, String, Float
from sqlalchemy.orm import relationship

association_table = Table('association',
                          Base.metadata,
                          Column('fund_id', ForeignKey('funds.id')),
                          Column('account_id', ForeignKey('accounts.id'))
                          )


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
    # type = Column(String(30), nullable=False)
    value: Float = Column(Float)

    funds = relationship('Fund', secondary=association_table,
                         back_populates='accounts')

    account_types_id = Column(Integer, ForeignKey("account_types.id"))
    account_type = relationship('AccountType', back_populates='accounts')

    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    portfolio = relationship('Portfolio', back_populates='accounts')

    def __repr__(self) -> str:
        return f"<Account {self.id}>"


class AccountType(Base):
    __tablename__ = 'account_types'
    id = Column(Integer, primary_key=True)
    type = Column(String(30), nullable=False, unique=True)
    transaction_fee = Column(Float)
    transaction_number = Column(Integer)
    annual_fee = Column(Float)

    accounts = relationship(
        'Account', back_populates='account_type', cascade='all, delete')

    def __repr__(self) -> str:
        return f"<AccountType {self.type}>"


class Fund(Base):
    __tablename__ = 'funds'

    id = Column(Integer, primary_key=True, autoincrement=True)
    isin = Column(String(12), nullable=False, unique=True)
    # name = Column(String(200))
    # nav = Column(Float)
    ofc = Column(Float)
    # fund_type = Column(Integer)
    # url = Column(String(200))

    accounts = relationship(
        'Account', secondary=association_table, back_populates='funds', cascade='all, delete')

    def __repr__(self) -> str:
        return f"<Fund {self.isin}>"
