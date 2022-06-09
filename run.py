"""
File used to test DB connector methods.
"""
from pprint import pprint
from unicodedata import name
from utils import yml_load
from dataclasses import dataclass
import logging
from database.base import Session
from database.connector import Connector
from database.db_tables import *
from populate import populate

import pandas as pd


def main():
    session = Session()
    db = Connector(session)

    # populate(db)

    portfolio = db.select(Portfolio, {'id': 1})

    db.session.delete(portfolio)

    # account_type = db.select(
    #     AccountType,
    #     {'type': 'vanguard'})

    # account = Account(value=123123,
    #                   account_type=account_type,
    #                   portfolio=portfolio
    #                   )

    # prt_load = yml_load('prt_load.yml')

    # account_type = db.session.query(
    #     AccountType).filter(AccountType.id == 2).first()

    # fund = db.session.query(Fund).filter(Fund.isin == "BBBB").first()

    # fund = db.select(Fund, {"isin": "AAAA"})

    # print(fund)
    # pprint(prt_load)

    # portfolio = Portfolio(name="portfolio_2")
    # account = Account(
    #     value=15000.6, account_type=account_type, portfolio=portfolio)

    # account = db.session.query(
    #     Account).filter(Account.id == 2).first()

    # print(f"{account}")

    # portfolio = db.session.query(
    #     Portfolio).filter(Portfolio.id == 2).first()

    # portfolio.accounts.append(account)
    # account.funds.append(fund)
    # print(account.funds)
    # print(account.account_type)
    # print(account.portfolio)

    db.session.commit()
    db.session_close()


if __name__ == '__main__':
    main()

    # data = {
    #     'isin': 'GB00B5B71H80',
    #     'name': 'Vanguard FTSE Developed Europe ex-U.K. Equity Index Fund GBP Acc',
    #     'nav': 310.04,
    #     'ofc': 0.12,
    #     'fund_type': 100
    # }

    # portfolio_template_yml = yml_load("portfolio_template.yml")

    # a = db.add_portfolio('portfolio.csv')
    # print(a)

    # df = pd.read_csv('portfolio.csv')

    # for i, row in df.iterrows():
    #     # print(row)
    #     # portfolio_id = row['portfolio']

    #     portfolio_id = db.select(Portfolio, {'name': row['portfolio']}).id
    #     account_id = db.select(Account, {'name': row['account']}).id
    #     fund_id = db.select(Fund, {'isin': row['fund']}).id

    #     data = {
    #         'portfolio_id': portfolio_id,
    #         'account_id': account_id,
    #         'fund_id': fund_id,
    #         'weight': row['weight']
    #     }

    #     # s = db.insert(Selection, data)

    #     print(s)

    # a = db.insert(Portfolio, data)

    # print(a)
    # print(a.id)

    # session.commit()

    # pprint(df)

    ############
    # data_update = {
    #     'ofc': 30,
    #     'nav': 60,
    # }

    # filter = {'isin': 'GB00B5B71H80'}
    # filter = {'fund_type': '100'}

    # u = db.update(Fund, filter, data_update)

    # print(u)

    # select_one = db.select(Fund, filter)

    # print(select_one)

    # for s, f in query:
    # #     print(s.__dict__)
    # #     print(f.__dict__)
    # #     print('')

    # for q in query:
    #     print(q.__dict__)
    # print(q.selection)
    #     print(q.account.name)
    #     print(q.fund.isin)
