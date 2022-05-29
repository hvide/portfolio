import typing
from .funds import Fund


class Account:
    def __init__(self, provider: str, value: float, funds: typing.List) -> object:
        """
        Collection of fund
        :param provider: Who is providing the fund
        :param value: Value of the account in £
        :param funds: list of funds
        """
        self.provider = provider
        self.value = value
        self.funds = funds

    def tot_actual_ofc(self) -> float:
        """
        OFC of the overall account by summing the actual_ofc together
        :return: (float)
        """
        x = [fund.actual_ofc() for fund in self.funds]
        return sum(x)

    def tot_actual_ofc_value(self) -> float:
        """
        Total of the actual OFC in £ by summing actual_ofc_value together
        :param value: Total value of the account in £
        :return: (float)
        """
        x = [fund.actual_ofc_value(self.value) for fund in self.funds]
        return sum(x)

    def equity_percent(self) -> float:
        x = [(fund.allocation_percent / 100) *
             fund.fund_type for fund in self.funds]
        return sum(x)

    def bond_percent(self) -> float:
        x = [(fund.allocation_percent / 100) * fund.bond_percent()
             for fund in self.funds]
        return sum(x)

    def unallocated_percent(self) -> float:
        return 100 - (self.equity_percent() + self.bond_percent())
