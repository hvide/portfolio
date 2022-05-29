from unittest import TestCase
from models.funds import Fund
from models.vanguard import Vanguard

funds = [
    Fund(isin="GB00B4PQW151", allocation_percent=50),
    Fund(isin="GB00B5B71Q71", allocation_percent=50),
]


class TestVanguard(TestCase):
    def setUp(self):
        self.account = Vanguard(
            provider="Vanguard_S&S", value=200, funds=funds)


class TestAnnualCost(TestVanguard):
    def test_annual_cost(self):
        self.assertEqual(self.account.annual_cost(), 0.30)


class TestTotAnnualCost(TestVanguard):
    def test_tot_annual_cost(self):
        self.assertEqual(self.account.tot_annual_cost(), 0.62)
