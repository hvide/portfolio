from database.db_tables import *


def populate(db):
    fund1 = Fund(isin="AAAA", ofc=0.21)
    fund2 = Fund(isin="BBBB", ofc=0.22)
    fund3 = Fund(isin="CCCC", ofc=0.23)
    fund4 = Fund(isin="DDDD", ofc=0.24)

    account_type1 = AccountType(
        type="iweb", annual_fee=0.15)
    account_type2 = AccountType(
        type="iweb", transaction_fee=5.0, transaction_number=2)

    account1 = Account(value=5000.0, account_type=account_type1)
    account2 = Account(value=15411.5, account_type=account_type2)

    db.session.add_all([fund1, fund2, fund3, fund4,
                       account_type1, account_type2, account1, account1])
