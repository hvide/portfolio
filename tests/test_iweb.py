from unittest import TestCase
from models.funds import Fund
from models.iweb import Iweb

funds = [
    Fund(isin="GB00B4PQW151", allocation_percent=50),
    Fund(isin="GB00B5B71Q71", allocation_percent=50),
]


class TestIweb(TestCase):
    def setUp(self):
        self.account = Iweb(provider="iWeb",
                            value=100, funds=funds, transaction_number=2)


class TestTotAnnualCost(TestIweb):
    def test_tot_annual_cost(self):
        self.assertEqual(self.account.tot_annual_cost(), 10)
