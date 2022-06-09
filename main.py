from unicodedata import name
from unittest import result
from utils import yml_load, jinja2_load
from pprint import pprint
import pandas as pd
import logging
from datetime import datetime
import sys
import os

from config import ROUND_N

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


def report():

    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.width', 1000)

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

                funds_list.append(Fund(
                    isin=fund, allocation_percent=allocation_percent))

            account_value = funds[0]['value']

            if provider == "Vanguard_S&S":
                account = Vanguard(provider, account_value, funds_list)
            elif provider == "iWeb":
                account = Iweb(provider, account_value, funds_list,
                               funds[0]['transaction_number'])
            else:
                logger.error(f"The provider: { provider } wasn't recognized")
                sys.exit(1)

            accounts_list.append(account)

            # df = pd.DataFrame([fund.to_dict(account_value) for fund in funds_list])

            # template = jinja2_load('fund.j2')
            # print(template.render(funds=[fund.to_dict(account_value) for fund in funds_list]))

            if PRINT_ACCOUNT == True:
                logger.info("Account list: %s" % account.provider)
                # print("Account name: %s" % account.provider)
                print("Account value: £ %s" % account.value)
                print("tot_actual_ofc: %s" %
                      round(account.tot_actual_ofc(), ROUND_N))
                print("tot_actual_ofc_value: £ %s" %
                      round(account.tot_actual_ofc_value(), ROUND_N))
                print("Account tot_annual_cost: £ %s" %
                      account.tot_annual_cost())
                print("Account Equity: %s  | Bond: %s" % (
                    round(account.equity_percent(), ROUND_N), round(account.bond_percent(), ROUND_N)))
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
                  round(portfolio.tot_annual_cost(), ROUND_N))
            print("Portfolio Equity: %s  | Bond: %s" % (
                round(portfolio.equity_percent(), ROUND_N), round(portfolio.bond_percent(), ROUND_N)))
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
            print("Target Value (Formula to be fixed):")

            target_value = portfolio.per_fund_target_percent()
            if target_value is not None:
                for tv in target_value:
                    print(tv)

            # print("Increase Bond (Formula to be fixed): %s" %
            #       portfolio.per_fund_bond_increase())

            # print(p_ref - pa)

            # logger.debug(portfolio.tot_value())
            # logger.debug(portfolio.bond_percent())
        print('')


def add_portfolio(db, conf_yml):

    conf = yml_load(conf_yml)

    pprint(conf['portfolio']['name'])

    portfolio = db_tables.Portfolio(name=conf['portfolio']['name'])
    # portfolio = db.select(db_tables.Portfolio, {'id': 1})
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

    portfolio_db = db.select(db_tables.Portfolio, {'id': 1})

    accounts = []
    for account_db in portfolio_db.accounts:

        funds = []
        for fund_db in account_db.funds:

            funds.append(Fund(fund_db.fund_type, fund_db.weight))
            # pprint(fund.to_dict(1))

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
            # print("Account name: %s" % account.provider)
            print("Account value: £ %s" % account.value)
            print("tot_actual_ofc: %s" %
                  round(account.tot_actual_ofc(), ROUND_N))
            print("tot_actual_ofc_value: £ %s" %
                  round(account.tot_actual_ofc_value(), ROUND_N))
            print("Account tot_annual_cost: £ %s" %
                  account.tot_annual_cost())
            print("Account Equity: %s  | Bond: %s" % (
                round(account.equity_percent(), ROUND_N), round(account.bond_percent(), ROUND_N)))
            print("Account unalocated percent: %s" %
                  account.unallocated_percent())
        if PRINT_FUND == True:
            df = pd.DataFrame([fund.to_dict(account_db.value)
                               for fund in funds])
            print(df)

        print('')

    if PRINT_PORTFOLIO == True:
        portfolio = Portfolio(portfolio_db.name, accounts)
        print("Portfolio tot_annual_cost: £ %s" %
              round(portfolio.tot_annual_cost(), ROUND_N))
        print("Portfolio Equity: %s  | Bond: %s" % (
            round(portfolio.equity_percent(), ROUND_N), round(portfolio.bond_percent(), ROUND_N)))
        print("Portfolio unalocated percent: %s" %
              round(portfolio.unallocated_percent(), 4))
        print("Ref: %s" % portfolio.account_a_equity_percent_target())
        print("Actual: %s" % portfolio.account_a_equity_percent_actual())
        print("Delta: %s" % portfolio.account_a_equity_percent_delta())
        print("Target Value (Formula to be fixed):")

        target_value = portfolio.per_fund_target_percent()
        if target_value is not None:
            for tv in target_value:
                print(tv)
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
            "Choose the program mode (report / report_db / update / reload / add_portfolio) [report_db]: ").lower()
        if mode == "":
            mode = "report_db"
            break
        elif mode == "report":
            break
        elif mode == "update":
            break
        elif mode == "reload":
            break
        elif mode == "add_portfolio":
            break

    if mode == "update":
        fund_info_update(db)

    elif mode == "report":
        report()

    elif mode == "report_db":
        report_db(db)

    elif mode == "reload":
        print(fund_info_add(db))

    elif mode == "add_portfolio":
        add_portfolio(db, 'prt_load.yml')

    db.session_close()
