import typing
from utils import yml_load


class Fund:
    def __init__(self, isin, allocation_percent):
        self.isin = isin
        self.funds_info = yml_load('funds_info.yml')
        self.name = self.funds_info[self.isin]['name']
        self.nav = self.funds_info[self.isin]['nav']
        self.ofc = self.funds_info[self.isin]['ofc']
        self.fund_type = self.funds_info[self.isin]['fund_type']
        # Percentage of the account allocated to this fund
        self.allocation_percent = allocation_percent

    def allocation_value(self, value):
        return (self.allocation_percent / 100) * value

    def ofc_percent(self):
        return self.ofc * 100

    def actual_ofc(self):
        """
        Actual OFC percentage over the value of the overall account
        :return:
        """
        return (self.allocation_percent / 100) * self.ofc

    def actual_ofc_value(self, value):
        """
        Actual OFC over the value of the account
        :param value: Value of the account
        :return:
        """
        return (self.allocation_value(value) / 100) * self.ofc

    def equity_percent(self):
        return self.fund_type

    def bond_percent(self):
        return 100 - self.fund_type

    def to_dict(self, value):
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
