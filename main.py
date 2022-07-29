from utils import yml_load
from pprint import pprint
import pandas as pd
import logging
from datetime import datetime
import sys
from tabulate import tabulate

from config import ROUND_N, PORTFOLIO_ID

from models.funds import Fund
from models.vanguard import Vanguard
from models.iweb import Iweb
from models.portfolios import Portfolio

from database.base import Session
from database.connector import Connector
from database import db_tables

import scraper


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

PRINT_FUND = True
PRINT_ACCOUNT = True
PRINT_PORTFOLIO = True


def fund_info_update(db):
    # funds = scraper.get_info()

    # session = Session()
    # db = Connector(session)

    funds = db.select_all(db_tables.FundType)

    results = []

    for fund in funds:

        data = scraper.get_info(fund.url)

        # data = {
        # 'nav': fund['nav'],
        # 'ofc': fund['ofc'],
        # }

        results.append(db.update(db_tables.FundType,
                       {'isin': fund.isin}, data))

    return results


def fund_info_add(db):

    # session = Session()
    # db = Connector(session)

    funds_info_load_yml = yml_load('funds_info_load.yml')

    data = []

    for fund in funds_info_load_yml:

        data.append(db.insert(db_tables.FundType, fund))

    logger.info(f"Data added to the database.")
    return data


def add_portfolio(db, conf_yml):

    conf = yml_load(conf_yml)

    pprint(conf['portfolio']['name'])

    portfolio = db_tables.Portfolio(name=conf['portfolio']['name'])
    logger.info(f"Portfolio: {portfolio}")

    for account_key in conf['accounts']:

        account_type = db.select(
            db_tables.AccountType,
            {'type': account_key})

        value = conf['accounts'][account_key]['info']['value']

        account = db_tables.Account(value=value,
                                    account_type=account_type,
                                    portfolio=portfolio
                                    )

        print(account)

        if account_key == 'iweb':
            account.transaction_number = conf['accounts'][account_key]['info']['transaction_number']

        logger.info(f"Account: {account}")

        for isin, weight in conf['accounts'][account_key]['funds'].items():

            fund_type = db.select(
                db_tables.FundType,
                {'isin': isin})

            fund = db_tables.Fund(weight=weight, fund_type=fund_type)
            account.funds.append(fund)

    db.session.commit()
    return portfolio


def report_db(db):

    portfolio_db = db.select(db_tables.Portfolio, {'id': PORTFOLIO_ID})

    accounts = []
    table = []
    for account_db in portfolio_db.accounts:

        funds = []
        for fund_db in account_db.funds:

            funds.append(Fund(fund_db.fund_type, fund_db.weight))

        provider = account_db.account_type.type

        if provider == 'vanguard':
            account = Vanguard(
                provider, account_db.value, funds)
        elif provider == 'iweb':
            account = Iweb(provider, account_db.value, funds,
                           account_db.transaction_number)
        else:
            logger.error(f"The provider: { provider } wasn't recognized")
            sys.exit(1)

        accounts.append(account)

        # Print details regarding Account
        if PRINT_ACCOUNT == True:
            logger.info("Account list: %s" % account.provider)

            row = [
                account.provider,
                account.value,
                round(account.tot_actual_ofc(), ROUND_N),
                round(account.tot_actual_ofc_value(), ROUND_N),
                round(account.tot_annual_cost(), ROUND_N),
                round(account.equity_percent(), ROUND_N),
                round(account.bond_percent(), ROUND_N),
                account.unallocated_percent(),
            ]
            table.append(row)

        if PRINT_FUND == True:
            df = pd.DataFrame([fund.to_dict(account_db.value)
                               for fund in funds])

            print(df)

    print("Accounts Table")
    print(tabulate(table, headers=["Provider",
          "Account value: £", "tot_actual_ofc", "tot_actual_ofc_value",
                                   "Account tot_annual_cost: £", "Equity %", "Bond %",
                                   "Account unalocated percent"], numalign="right"))

    print('')

    if PRINT_PORTFOLIO == True:
        portfolio = Portfolio(portfolio_db.name, accounts)

        table = [
            portfolio.name,
            round(portfolio.tot_annual_cost(), ROUND_N),
            round(portfolio.equity_percent(), ROUND_N),
            round(portfolio.bond_percent(), ROUND_N),
            round(portfolio.unallocated_percent(), 4),
            portfolio.account_a_equity_percent_target(),
            portfolio.account_a_equity_percent_actual(),
            portfolio.account_a_equity_percent_delta(),
        ]

        headers = [
            "Portfolio Name",
            "Portfolio tot_annual_cost: £",
            "Equity %",
            "Bond %",
            "Portfolio unalocated percent",
            "Ref",
            "Actual",
            "Delta",
        ]

        print('')
        print(tabulate([table], headers=headers, numalign="right"))
        print('')

        target_value = portfolio.per_fund_target_percent()
        if target_value is not None:
            for tv in target_value:
                print(tv)

            x = zip(target_value, portfolio.accounts[0].funds)

            for y in x:
                y[1].weight = y[0]['target_percent']
        print("Portfolio tot_annual_cost updated: £ %s" %
              round(portfolio.tot_annual_cost(), ROUND_N))

    print('')
    # print(portfolio)


if __name__ == '__main__':

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)

    session = Session()
    db = Connector(session)

    while True:
        mode = input(
            "Choose the program mode ( report_db / update / reload / add_portfolio) [report_db]: ").lower()
        if mode == "":
            mode = "report_db"
            break
        elif mode == "update":
            break
        elif mode == "reload":
            break
        elif mode == "add_portfolio":
            break

    if mode == "update":
        fund_info_update(db)

    elif mode == "report_db":
        report_db(db)

    elif mode == "reload":
        print(fund_info_add(db))

    elif mode == "add_portfolio":
        add_portfolio(db, 'new_portfolio.yml')

    db.session_close()
