from helpers import yml_load, jinja2_load
from pprint import pprint
import pandas as pd
import logging
from datetime import datetime
import sys, os

__author__ = 'Davide Gilardoni'
__email__ = 'dade_gila@hotmail.com'
__version__ = '0.0.1'

# Logging setup

DATE_STAMP = datetime.now().strftime("%d_%m_%y_%H%M%S")
LOG_LEVEL = logging.INFO

logger = logging.getLogger('logger')
logger.setLevel(LOG_LEVEL)

screen_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S")
screen = logging.StreamHandler(sys.stdout)
screen.setFormatter(screen_formatter)
logger.addHandler(screen)


class Portfolio:
    def __init__(self, name, accounts):
        self.name = name
        self.accounts = accounts

    def tot_value(self):
        x = [account.value for account in self.accounts]
        return sum(x)

    def tot_equity_value(self):
        x = [account.value for account in self.accounts]
        return sum(x)

    def equity_percent(self):
        x = [account.equity_percent() for account in self.accounts]
        y = sum(x) / len(self.accounts)
        return y

    def bond_percent(self):
        x = [account.bond_percent() for account in self.accounts]
        y = sum(x) / len(self.accounts)
        return y

    def unallocated_percent(self):
        return 100 - (self.equity_percent() + self.bond_percent())


class Account:
    def __init__(self, provider, value, funds):
        """
        Collection of fund
        :param provider: Who is providing the fund
        :param value: Value of the account in £
        :param funds: list of funds
        """
        self.provider = provider
        self.value = value
        self.funds = funds

    def tot_actual_ofc(self):
        """
        Calculate OFC of the overall account by summing the actual_ofc together
        :return:
        """
        x = [fund.actual_ofc() for fund in self.funds]
        return sum(x)

    def tot_actual_ofc_value(self, value):
        """
        Calculate Total of the actual OFC in £ by summing actual_ofc_value together
        :param value: Total value of the account in £
        :return:
        """
        x = [fund.actual_ofc_value(value) for fund in self.funds]
        return sum(x)

    def equity_percent(self):
        x = [fund.allocation_percent for fund in self.funds if fund.fund_type == "equity"]
        return sum(x)

    def bond_percent(self):
        x = [fund.allocation_percent for fund in self.funds if fund.fund_type == "bond"]
        return sum(x)

    def unallocated_percent(self):
        return 100 - (self.equity_percent() + self.bond_percent())

class Fund:
    def __init__(self, isin, name, nav, ofc, fund_type, allocation_percent):
        self.isin = isin
        self.name = name
        self.nav = nav
        self.ofc = ofc
        self.fund_type = fund_type
        self.allocation_percent = allocation_percent

    def allocation_value(self, value):
        return (self.allocation_percent / 100) * value

    def ofc_percent(self):
        return self.ofc * 100

    def actual_ofc(self):
        return (self.allocation_percent / 100) * self.ofc

    def actual_ofc_value(self, value):
        return (self.allocation_value(value) / 100) * self.ofc

    def to_dict(self, value):
        return {
            'isin': self.isin,
            'name': self.name,
            'allocation_percent': self.allocation_percent,
            'nav': self.nav,
            'ofc': self.ofc,
            'fund_type': self.fund_type,
            'actual_ofc': self.actual_ofc(),
            'allocation_value': self.allocation_value(value),
            'actual_ofc_value': self.actual_ofc_value(value)

        }


def main():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)

    funds_info_yml = yml_load('funds_info.yml')
    portfolios_yml = yml_load('portfolios.yml')

    for prtf, acc in portfolios_yml.items():
    # for portfolio in portfolios_yml['portfolios']:
        print('########################')
        print(prtf)
        accounts_list = []
        for p, funds in acc.items():
            funds_list = []
            # test = portfolios_yml[p]
            # print("Account name: %s" % p)
            for fund in funds[1]:
                # print(p)
                # print(funds[fund])
                fund_obj = Fund(isin=fund,
                                name=funds_info_yml[fund]['name'],
                                nav=funds_info_yml[fund]['nav'],
                                ofc=funds_info_yml[fund]['ofc'],
                                fund_type=funds_info_yml[fund]['fund_type'],
                                allocation_percent=funds[1][fund])
                funds_list.append(fund_obj)

                # print(fund.__dict__)
                # print(fund.allocation_value(portfolios_yml['value']))
                # print(fund.ofc_percent())
                # print(fund.actual_ofc())
                # print(fund.actual_ofc_value(portfolios_yml['value']))

            account_value = funds[0]['value']
            account = Account(p, account_value, funds_list)
            accounts_list.append(account)
            df = pd.DataFrame([p.to_dict(account_value) for p in funds_list])
            print("Account name: %s" % account.provider)
            print("Account value: £ %s" % account.value)
            print("tot_actual_ofc: %s" % account.tot_actual_ofc())
            print("tot_actual_ofc_value: £ %s" % account.tot_actual_ofc_value(account_value))
            print("Account Equity: %s  | Bond: %s" % (account.equity_percent(), account.bond_percent()))
            print("Account unalocated percent: %s" % account.unallocated_percent())
            # print(df)
            logger.debug(df)
            print('')
        portfolio = Portfolio(prtf, accounts_list)
        print("Portfolio Equity: %s  | Bond: %s" % (portfolio.equity_percent(), portfolio.bond_percent()))
        print("Portfolio unalocated percent: %s" % portfolio.unallocated_percent())
        logger.debug(portfolio.tot_value())
        logger.debug(portfolio.bond_percent())
        print('')


if __name__ == '__main__':
    main()


