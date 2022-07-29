from unittest import TestCase
from models.funds import Fund
from database.base import Session
from database.connector import Connector
from database import db_tables


session = Session()
db = Connector(session)


class TestFund(TestCase):
    def setUp(self):

        fund_type = db.select(db_tables.FundType, {'isin': 'GB00B4PQW151'})

        self.fund = Fund(fund_type=fund_type, weight=20)


class TestEquityPercent(TestFund):
    def test_equity_percent(self):
        self.assertEqual(self.fund.equity_pct, self.fund.equity_percent())
        # print(self.fund.__dict__)


class TestBondPercent(TestFund):
    def test_bond_percent(self):
        self.fund.equity_pct = 80
        self.assertEqual(self.fund.bond_percent(), 20)
        # print(self.fund.__dict__)


class TestOfcPercent(TestFund):
    def test_ofc_percent(self):
        self.assertEqual(self.fund.ofc_percent(), 22)


class TestAllocationValue(TestFund):
    def test_allocation_value(self):
        self.assertEqual(self.fund.allocation_value(1000), 200)


class TestActualOfc(TestFund):
    def test_actual_ofc(self):
        self.fund.ofc = 0.24
        self.fund.allocation_percent = 22
        self.assertEqual(self.fund.actual_ofc(), 0.048)


class TestActualOfcValue(TestFund):
    def test_actual_ofc_value(self):
        self.assertEqual(self.fund.actual_ofc_value(1000), 0.44)
