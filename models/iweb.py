import typing
from models.accounts import Account


class Iweb(Account):
    def __init__(self, provider: str, value: float, funds: typing.List, transaction_number: int) -> object:
        super(Iweb, self).__init__(provider, value, funds)
        self.transaction_number = transaction_number
        self.transaction_fee = 5

    def tot_annual_cost(self) -> float:
        return (self.transaction_fee * self.transaction_number) + self.tot_actual_ofc_value()
