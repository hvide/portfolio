from asyncio.log import logger
import logging
import typing
import sys
import os
from config import ROUND_N, EQUITY_TARGET

sys.path.insert(1, os.path.join(sys.path[0], '..'))

logger = logging.getLogger()


class Portfolio:
    def __init__(self, name: str, accounts):
        self.name = name
        self.accounts = accounts

    def tot_value(self) -> float:
        """
        Total value of the portfolio
        """
        x = [account.value for account in self.accounts]
        return sum(x)

    def equity_percent(self) -> float:
        x = [(account.value * account.equity_percent())
             for account in self.accounts]
        y = sum(x) / self.tot_value()
        return y

    def bond_percent(self) -> float:
        x = [(account.value * account.bond_percent())
             for account in self.accounts]
        y = sum(x) / self.tot_value()
        return y

    def unallocated_percent(self) -> float:
        return 100 - (self.equity_percent() + self.bond_percent())

    def tot_annual_cost(self: float) -> float:
        """
        Total annual cost of the portfolio
        """
        x = [account.tot_annual_cost()
             for account in self.accounts]
        return sum(x)

    def account_a_equity_percent_target(self) -> float:
        return ((self.tot_value() * EQUITY_TARGET) - (self.accounts[1].value * self.accounts[1].equity_percent())) / self.accounts[0].value

    def account_a_equity_percent_actual(self) -> float:
        return ((self.tot_value() * self.equity_percent()) - (self.accounts[1].value * self.accounts[1].equity_percent())) / self.accounts[0].value

    def account_a_equity_percent_delta(self) -> float:
        return self.account_a_equity_percent_target() - self.account_a_equity_percent_actual()

    def per_fund_target_percent(self) -> typing.List:
        """
        Not working as expected, to be fixed
        :return:
        """
        f = []
        for fund in self.accounts[0].funds:

            if fund.fund_type == 100:
                target_percent = (fund.allocation_percent / self.accounts[0].equity_percent(
                ) * self.account_a_equity_percent_target())

                target_value = self.accounts[0].value * target_percent / 100

            elif fund.fund_type == 0:
                target_percent = (fund.allocation_percent / self.accounts[0].bond_percent() * (
                    100 - self.account_a_equity_percent_target()))

                target_value = self.accounts[0].value * target_percent / 100

            else:
                logger.warn(
                    f"This method doesn't work with funds which are mix of equity and bonds: { fund.isin }")
                return None

            data = {
                'isin': fund.isin,
                'target_percent': round(target_percent, ROUND_N),
                'target_value': round(target_value, ROUND_N),
            }
            f.append(data)

        return f
