from database.db_tables import *


def populate(db):

    account_type1 = AccountType(
        type="vanguard", annual_fee=0.15)
    account_type2 = AccountType(
        type="iweb", transaction_fee=5.0)

    # account1 = Account(value=5000.0, account_type=account_type1)
    # account2 = Account(value=15411.5, account_type=account_type2)

    db.session.add_all([
        # fund1,
        # fund2,
        # fund3,
        # fund4,
        account_type1,
        account_type2,
        # account1,
        # account1
    ])
