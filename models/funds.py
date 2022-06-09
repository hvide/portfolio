import typing
from utils import yml_load


class Fund:
    def __init__(self, fund_type: str, weight: float) -> object:
        self.isin: str = fund_type.isin
        # # self.funds_info: typing.Dict = yml_load('funds_info.yml')
        # self.name: str = self.funds_info[self.isin]['name']
        # self.nav: float = self.funds_info[self.isin]['nav']
        # self.ofc: float = self.funds_info[self.isin]['ofc']
        # self.equity_pct: int = self.funds_info[self.isin]['equity_pct']
        # # Percentage of the account allocated to this fund
        # self.allocation_percent: float = allocation_percent

        self.name: str = fund_type.name
        self.nav: float = fund_type.nav
        self.ofc: float = fund_type.ofc
        self.equity_pct: int = fund_type.equity_pct
        self.allocation_percent: float = weight

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
        return self.equity_pct

    def bond_percent(self) -> float:
        return 100 - self.equity_pct

    def to_dict(self, value: float) -> typing.Dict:
        return {
            'isin': self.isin,
            'name': self.name,
            'allocation_percent': self.allocation_percent,
            'nav': self.nav,
            'ofc': self.ofc,
            'equity_pct': self.equity_pct,
            'actual_ofc': self.actual_ofc(),
            'allocation_value': self.allocation_value(value),
            'actual_ofc_value': self.actual_ofc_value(value)

        }

    def __repr__(self) -> str:
        return f"<Fund {self.isin}>"
