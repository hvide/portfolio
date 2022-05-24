from utils import yml_load, jinja2_load
from pprint import pprint
import pandas as pd
import logging
from datetime import datetime
import sys
import os

from models.funds import Fund
from models.accounts import Account
from models.portfolios import Portfolio

__author__ = 'Davide Gilardoni'
__email__ = 'dade_gila@hotmail.com'
__version__ = '1.0.2'

# Logging setup

DATE_STAMP = datetime.now().strftime("%d_%m_%y_%H%M%S")
LOG_LEVEL = logging.DEBUG
# LOG_LEVEL = logging.INFO

logger = logging.getLogger('logger')
logger.setLevel(LOG_LEVEL)

screen_formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S")
screen = logging.StreamHandler(sys.stdout)
screen.setFormatter(screen_formatter)
logger.addHandler(screen)
n = 2  # Number of decimals
PRINT_FUND = False
PRINT_ACCOUNT = True
PRINT_PORTFOLIO = True


def main():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)

    # funds_info_yml = yml_load('funds_info.yml')
    portfolios_yml = yml_load('portfolios.yml')

    for prtf, acc in portfolios_yml.items():
        # for portfolio in portfolios_yml['portfolios']:
        print('########################')
        # print(prtf)
        logger.info("Portfolio name: %s" % prtf)
        accounts_list = []
        for provider, funds in acc.items():
            funds_list = []
            for fund, allocation_percent in funds[1].items():
                # print(funds[1][fund])
                funds_list.append(Fund(
                    isin=fund, allocation_percent=allocation_percent))

            account_value = funds[0]['value']
            account = Account(provider, account_value, funds_list)
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
                print("tot_actual_ofc: %s" %
                      round(account.tot_actual_ofc(), n))
                print("tot_actual_ofc_value: £ %s" %
                      round(account.tot_actual_ofc_value(account_value), n))
                print("Account tot_annual_cost: £ %s" %
                      account.tot_annual_cost(account.value))
                print("Account Equity: %s  | Bond: %s" % (
                    round(account.equity_percent(), n), round(account.bond_percent(), n)))
                print("Account unalocated percent: %s" %
                      account.unallocated_percent())
                if PRINT_FUND == True:
                    df = pd.DataFrame([fund.to_dict(account_value)
                                      for fund in funds_list])
                    print(df)
                # logger.debug("\ns%" % df)
                print('')
        if PRINT_PORTFOLIO == True:
            portfolio = Portfolio(prtf, accounts_list)
            print("Portfolio tot_annual_cost: £ %s" %
                  round(portfolio.tot_annual_cost(), n))
            print("Portfolio Equity: %s  | Bond: %s" % (
                round(portfolio.equity_percent(), n), round(portfolio.bond_percent(), n)))
            print("Portfolio unalocated percent: %s" %
                  round(portfolio.unallocated_percent(), 4))

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
            print("Increase Equity (Formula to be fixed): %s" %
                  portfolio.per_fund_equity_increase())
            print("Increase Bond (Formula to be fixed): %s" %
                  portfolio.per_fund_bond_increase())

            # print(p_ref - pa)

            # logger.debug(portfolio.tot_value())
            # logger.debug(portfolio.bond_percent())
        print('')


if __name__ == '__main__':
    main()
