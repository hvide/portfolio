import typing
from models.accounts import Account


class Vanguard(Account):
    def __init__(self, provider: str, value: float, funds: typing.List) -> object:
        super(Vanguard, self).__init__(provider, value, funds)
        self.annual_fee = 0.15

    def annual_cost(self):
        """
        Annual cost of the account, percentage of the total value
        :return: (float)
        """
        return self.value / 100 * self.annual_fee

    def tot_annual_cost(self):
        return self.annual_cost() + self.tot_actual_ofc_value()
