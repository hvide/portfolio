import typing


class Account:
    def __init__(self, provider, value, funds, annual_fee=0, transaction_fee=0, transaction_number=0):
        """
        Collection of fund
        :param provider: Who is providing the fund
        :param value: Value of the account in £
        :param funds: list of funds
        """
        self.provider = provider
        self.value = value
        self.funds = funds
        self.annual_fee = annual_fee
        self.transaction_fee = transaction_fee
        self.transaction_number = transaction_number

    def tot_actual_ofc(self):
        """
        OFC of the overall account by summing the actual_ofc together
        :return: (float)
        """
        x = [fund.actual_ofc() for fund in self.funds]
        return sum(x)

    def tot_actual_ofc_value(self, value):
        """
        Total of the actual OFC in £ by summing actual_ofc_value together
        :param value: Total value of the account in £
        :return: (float)
        """
        x = [fund.actual_ofc_value(value) for fund in self.funds]
        return sum(x)

    def equity_percent(self):
        x = [(fund.allocation_percent / 100) *
             fund.fund_type for fund in self.funds]
        return sum(x)

    def bond_percent(self):
        x = [(fund.allocation_percent / 100) * fund.bond_percent()
             for fund in self.funds]
        return sum(x)

    def unallocated_percent(self):
        return 100 - (self.equity_percent() + self.bond_percent())

    def tot_transaction_fee(self):
        """
        Sum of all transaction value
        :return:
        """
        return self.transaction_fee * self.transaction_number

    def annual_cost(self):
        """
        Annual cost of the account, percentage of the total value
        :return: (float)
        """
        return self.value / 100 * self.annual_fee

    def tot_annual_cost(self, value):
        return self.annual_cost() + self.tot_actual_ofc_value(value) + self.tot_transaction_fee()
