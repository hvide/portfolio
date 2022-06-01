"""
File used to test DB connector methods.
"""

import logging
from database.base import Session
from database.connector import Connector
from database.db_funds import Fund


def main():
    session = Session()
    db = Connector(session)

    # data = {
    #     'isin': 'GB00B5B71H80',
    #     'name': 'Vanguard FTSE Developed Europe ex-U.K. Equity Index Fund GBP Acc',
    #     'nav': 310.04,
    #     'ofc': 0.12,
    #     'fund_type': 100
    # }

    # a = db.insert(Fund, data)

    # print(a)

    # session.commit()

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

    query = db.select_all(Fund)
    # query = db.select_all(Fund, filter)

    for q in query:
        print(q.__dict__)

    db.session_close()


if __name__ == '__main__':
    main()
