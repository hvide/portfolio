from unittest import TestCase
from models.funds import Fund
from models.accounts import Account

funds = [
    Fund(isin="GB00B4PQW151", allocation_percent=50),
    Fund(isin="GB00B5B71Q71", allocation_percent=50),
]


class TestAccount(TestCase):
    def setUp(self):
        self.account = Account(provider="Vanguard_S&S", value=200, funds=funds)


class TestEquityPercent(TestAccount):
    def test_equity_percent(self):
        self.assertEqual(self.account.equity_percent(), 90)


class TestBondPercent(TestAccount):
    def test_bond_percent(self):
        self.assertEqual(self.account.bond_percent(), 100 -
                         self.account.equity_percent())


class TestTotActualOfc(TestAccount):
    def test_tot_actual_ofc(self):
        self.assertEqual(self.account.tot_actual_ofc(), 0.16)


class TestTotActualOfcValue(TestAccount):
    def test_tot_actual_ofc_value(self):
        self.assertEqual(self.account.tot_actual_ofc_value(), 0.32)
