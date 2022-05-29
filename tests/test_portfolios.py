from unittest import TestCase
from models.funds import Fund
from models.vanguard import Vanguard
from models.iweb import Iweb
from models.portfolios import Portfolio
from config import ROUND_N, EQUITY_TARGET

funds_1 = [
    Fund(isin="GB00B4PQW151", allocation_percent=50),
    Fund(isin="GB00B5B71Q71", allocation_percent=50),
]

funds_2 = [
    Fund(isin="GB00BF0GWY02", allocation_percent=50),
    Fund(isin="GB00B5B71Q71", allocation_percent=50),
]


class TestPortfolio(TestCase):
    def setUp(self):
        self.account = Portfolio(name="Test_Portfolio", accounts=[
            Vanguard(provider="Vanguard_S&S", value=200, funds=funds_1),
            Iweb(provider="iWeb", value=200,
                 funds=funds_2, transaction_number=2),
        ])


class TestTotValue(TestPortfolio):
    def test_tot_value(self):
        self.assertEqual(self.account.tot_value(), 400)


class TestTotAnnualCost(TestPortfolio):
    def test_tot_annual_cost(self):
        self.assertEqual(self.account.tot_annual_cost(), 10.84)
