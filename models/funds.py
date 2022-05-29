import typing
from utils import yml_load


class Fund:
    def __init__(self, isin: str, allocation_percent: float) -> object:
        self.isin: str = isin
        self.funds_info: typing.Dict = yml_load('funds_info.yml')
        self.name: str = self.funds_info[self.isin]['name']
        self.nav: float = self.funds_info[self.isin]['nav']
        self.ofc: float = self.funds_info[self.isin]['ofc']
        self.fund_type: int = self.funds_info[self.isin]['fund_type']
        # Percentage of the account allocated to this fund
        self.allocation_percent: float = allocation_percent

    def allocation_value(self, value: float) -> float:
        return (self.allocation_percent / 100) * value

    def ofc_percent(self) -> float:
        return self.ofc * 100

    def actual_ofc(self) -> float:
        """
        Actual OFC percentage over the value of the overall account
        :return:
        """
        return (self.allocation_percent / 100) * self.ofc

    def actual_ofc_value(self, value: float) -> float:
        """
        Actual OFC over the value of the account
        :param value: Value of the account
        :return:
        """
        return (self.allocation_value(value) / 100) * self.ofc

    def equity_percent(self) -> float:
        return self.fund_type

    def bond_percent(self) -> float:
        return 100 - self.fund_type

    def to_dict(self, value: float) -> typing.Dict:
        return {
            'isin': self.isin,
            'name': self.name,
            'allocation_percent': self.allocation_percent,
            'nav': self.nav,
            'ofc': self.ofc,
            'fund_type': self.fund_type,
            'actual_ofc': self.actual_ofc(),
            'allocation_value': self.allocation_value(value),
            'actual_ofc_value': self.actual_ofc_value(value)

        }
