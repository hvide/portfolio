# coding=utf-8

from dataclasses import dataclass
from sqlalchemy import Column, Float, String, Integer
from sqlalchemy.orm import relationship

from database.base import Base
from database.db_portfolios import Portfolio


class Fund(Base):
    __tablename__ = 'funds'

    isin = Column(String(16), primary_key=True, autoincrement=False)
    name = Column(String(200))
    nav = Column(Float)
    ofc = Column(Float)
    fund_type = Column(Integer)
    url = Column(String(200))

    def __init__(self, isin, name, nav, ofc, fund_type):
        self.isin = isin
        self.name = name
        self.nav = nav
        self.ofc = ofc
        self.fund_type = fund_type

    def __repr__(self) -> str:
        return self.isin
