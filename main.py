from helpers import yml_load, jinja2_load
from pprint import pprint
import pandas as pd
import logging
from datetime import datetime
import sys, os

__author__ = 'Davide Gilardoni'
__email__ = 'dade_gila@hotmail.com'
__version__ = '1.0.1'

# Logging setup

DATE_STAMP = datetime.now().strftime("%d_%m_%y_%H%M%S")
LOG_LEVEL = logging.DEBUG
# LOG_LEVEL = logging.INFO

logger = logging.getLogger('logger')
logger.setLevel(LOG_LEVEL)

screen_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S")
screen = logging.StreamHandler(sys.stdout)
screen.setFormatter(screen_formatter)
logger.addHandler(screen)
n = 2  # Number of decimals
PRINT_FUND = False
PRINT_ACCOUNT = True
PRINT_PORTFOLIO = True


class Portfolio:
    def __init__(self, name, accounts):
        self.name = name
        self.accounts = accounts

    def tot_value(self):
        x = [account.value for account in self.accounts]
        return sum(x)

    # def tot_equity_value(self):
    #     x = [account.value for account in self.accounts]
    #     return sum(x)

    def equity_percent(self):
        x = [(account.value * account.equity_percent()) for account in self.accounts]
        y = sum(x) / self.tot_value()
        return y

    def bond_percent(self):
        x = [(account.value * account.bond_percent()) for account in self.accounts]
        y = sum(x) / self.tot_value()
        return y

    def unallocated_percent(self):
        return 100 - (self.equity_percent() + self.bond_percent())

    def tot_annual_cost(self):
        x = [account.tot_annual_cost(account.value) for account in self.accounts]
        return sum(x)

    def account_a_equity_percent_target(self):
        return ((self.tot_value() * 80) - (self.accounts[1].value * self.accounts[1].equity_percent())) / self.accounts[0].value

    def account_a_equity_percent_actual(self):
        return ((self.tot_value() * self.equity_percent()) - (self.accounts[1].value * self.accounts[1].equity_percent())) / self.accounts[0].value

    def account_a_equity_percent_delta(self):
        return self.account_a_equity_percent_target() - self.account_a_equity_percent_actual()

    def per_fund_equity_increase(self):
        """
        Not working as expected, to be fixed
        :return:
        """
        return [round((fund.allocation_percent / self.accounts[0].equity_percent() * self.account_a_equity_percent_target()), n) for fund in self.accounts[0].funds]

    def per_fund_bond_increase(self):
        """
        Not working as expected, to be fixed
        :return:
        """
        return [round((fund.allocation_percent / self.accounts[0].bond_percent() * (100 - self.account_a_equity_percent_target())), n) for fund in self.accounts[0].funds]


class Account:
    def __init__(self, provider, value, funds, annual_fee=0, transaction_fee=0, transaction_number=0):
        """
        Collection of fund
        :param provider: Who is providing the fund
        :param value: Value of the account in £
        :param funds: list of funds
        """
        self.provider = provider
        self.value = value
        self.funds = funds
        self.annual_fee = annual_fee
        self.transaction_fee = transaction_fee
        self.transaction_number = transaction_number

    def tot_actual_ofc(self):
        """
        OFC of the overall account by summing the actual_ofc together
        :return: (float)
        """
        x = [fund.actual_ofc() for fund in self.funds]
        return sum(x)

    def tot_actual_ofc_value(self, value):
        """
        Total of the actual OFC in £ by summing actual_ofc_value together
        :param value: Total value of the account in £
        :return: (float)
        """
        x = [fund.actual_ofc_value(value) for fund in self.funds]
        return sum(x)

    def equity_percent(self):
        x = [(fund.allocation_percent / 100) * fund.fund_type for fund in self.funds]
        return sum(x)

    def bond_percent(self):
        x = [(fund.allocation_percent / 100) * fund.bond_percent() for fund in self.funds]
        return sum(x)

    def unallocated_percent(self):
        return 100 - (self.equity_percent() + self.bond_percent())

    def tot_transaction_fee(self):
        """
        Sum of all transaction value
        :return:
        """
        return self.transaction_fee * self.transaction_number

    def annual_cost(self):
        """
        Annual cost of the account, percentage of the total value
        :return: (float)
        """
        return self.value / 100 * self.annual_fee

    def tot_annual_cost(self, value):
        return self.annual_cost() + self.tot_actual_ofc_value(value) + self.tot_transaction_fee()


class Fund:
    def __init__(self, isin, name, nav, ofc, fund_type, allocation_percent):
        self.isin = isin
        self.name = name
        self.nav = nav
        self.ofc = ofc
        self.fund_type = fund_type
        self.allocation_percent = allocation_percent  # Percentage of the account allocated to this fund

    def allocation_value(self, value):
        return (self.allocation_percent / 100) * value

    def ofc_percent(self):
        return self.ofc * 100

    def actual_ofc(self):
        """
        Actual OFC percentage over the value of the overall account
        :return:
        """
        return (self.allocation_percent / 100) * self.ofc

    def actual_ofc_value(self, value):
        """
        Actual OFC over the value of the account
        :param value: Value of the account
        :return:
        """
        return (self.allocation_value(value) / 100) * self.ofc

    def equity_percent(self):
        return self.fund_type

    def bond_percent(self):
        return 100 - self.fund_type

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
        # print(prtf)
        logger.info("Portfolio name: %s" % prtf)
        accounts_list = []
        for p, funds in acc.items():
            funds_list = []
            for fund in funds[1]:
                fund_obj = Fund(isin=fund,
                                name=funds_info_yml[fund]['name'],
                                nav=funds_info_yml[fund]['nav'],
                                ofc=funds_info_yml[fund]['ofc'],
                                fund_type=funds_info_yml[fund]['fund_type'],
                                allocation_percent=funds[1][fund])
                funds_list.append(fund_obj)

            account_value = funds[0]['value']
            account = Account(p, account_value, funds_list)
            if 'annual_fee' in funds[0]:
                account.annual_fee = funds[0]['annual_fee']
            if 'transaction_fee' in funds[0]:
                account.transaction_fee = funds[0]['transaction_fee']
            if 'transaction_number' in funds[0]:
                account.transaction_number = funds[0]['transaction_number']
            accounts_list.append(account)
            # df = pd.DataFrame([fund.to_dict(account_value) for fund in funds_list])


            # template = jinja2_load('fund.j2')
            # print(template.render(funds=[fund.to_dict(account_value) for fund in funds_list]))

            if PRINT_ACCOUNT == True:
                logger.info("Account list: %s" % account.provider)
                # print("Account name: %s" % account.provider)
                print("Account value: £ %s" % account.value)
                print("tot_actual_ofc: %s" % round(account.tot_actual_ofc(), n))
                print("tot_actual_ofc_value: £ %s" % round(account.tot_actual_ofc_value(account_value), n))
                print("Account tot_annual_cost: £ %s" % account.tot_annual_cost(account.value))
                print("Account Equity: %s  | Bond: %s" % (round(account.equity_percent(), n), round(account.bond_percent(), n)))
                print("Account unalocated percent: %s" % account.unallocated_percent())
                if PRINT_FUND == True:
                    df = pd.DataFrame([fund.to_dict(account_value) for fund in funds_list])
                    print(df)
                # logger.debug("\ns%" % df)
                print('')
        if PRINT_PORTFOLIO == True:
            portfolio = Portfolio(prtf, accounts_list)
            print("Portfolio tot_annual_cost: £ %s" % round(portfolio.tot_annual_cost(), n))
            print("Portfolio Equity: %s  | Bond: %s" % (round(portfolio.equity_percent(), n), round(portfolio.bond_percent(), n)))
            print("Portfolio unalocated percent: %s" % round(portfolio.unallocated_percent(), 4))


            # t = portfolio.tot_value()
            # p = portfolio.bond_percent()
            # v = t / 100 * p
            # print(v)

            # tt = portfolio.tot_value()
            # pt = portfolio.equity_percent()
            # tb = portfolio.accounts[1].value
            # pb = portfolio.accounts[1].equity_percent()
            # ta = portfolio.accounts[0].value
            # pa = ((tt * pt) - (tb * pb)) / ta
            # print(pa)
            #
            # p_ref = ((tt * 80) - (tb * pb)) / ta
            # print(p_ref)
            print("Ref: %s" % portfolio.account_a_equity_percent_target())
            print("Actual: %s" % portfolio.account_a_equity_percent_actual())
            print("Delta: %s" % portfolio.account_a_equity_percent_delta())
            print("Increase Equity (Formula to be fixed): %s" % portfolio.per_fund_equity_increase())
            print("Increase Bond (Formula to be fixed): %s" % portfolio.per_fund_bond_increase())

            # print(p_ref - pa)


            # logger.debug(portfolio.tot_value())
            # logger.debug(portfolio.bond_percent())
        print('')


if __name__ == '__main__':
    main()


