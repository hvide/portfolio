from unittest import TestCase
from main import Fund


# class TestFund(TestCase):
#     def test_equity_percent(self):
#         self.fail()


class TestFund(TestCase):
    def setUp(self):
        self.fund = Fund(isin="ISIN1234",
                         name="MyName",
                         nav=274,
                         ofc=0.22,
                         fund_type=100,
                         allocation_percent=20)


class TestEquityPercent(TestFund):
    def test_equity_percent(self):
        self.assertEqual(self.fund.fund_type, self.fund.equity_percent())
        # print(self.fund.__dict__)


class TestBondPercent(TestFund):
    def test_bond_percent(self):
        self.fund.fund_type = 80
        self.assertEqual(self.fund.bond_percent(), 20)
        # print(self.fund.__dict__)


