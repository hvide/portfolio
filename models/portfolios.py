import typing


class Portfolio:
    def __init__(self, name, accounts):
        self.name = name
        self.accounts = accounts

    def tot_value(self):
        x = [account.value for account in self.accounts]
        return sum(x)

    # def tot_equity_value(self):
    #     x = [account.value for account in self.accounts]
    #     return sum(x)

    def equity_percent(self):
        x = [(account.value * account.equity_percent())
             for account in self.accounts]
        y = sum(x) / self.tot_value()
        return y

    def bond_percent(self):
        x = [(account.value * account.bond_percent())
             for account in self.accounts]
        y = sum(x) / self.tot_value()
        return y

    def unallocated_percent(self):
        return 100 - (self.equity_percent() + self.bond_percent())

    def tot_annual_cost(self):
        x = [account.tot_annual_cost(account.value)
             for account in self.accounts]
        return sum(x)

    def account_a_equity_percent_target(self):
        return ((self.tot_value() * 80) - (self.accounts[1].value * self.accounts[1].equity_percent())) / self.accounts[0].value

    def account_a_equity_percent_actual(self):
        return ((self.tot_value() * self.equity_percent()) - (self.accounts[1].value * self.accounts[1].equity_percent())) / self.accounts[0].value

    def account_a_equity_percent_delta(self):
        return self.account_a_equity_percent_target() - self.account_a_equity_percent_actual()

    def per_fund_equity_increase(self):
        """
        Not working as expected, to be fixed
        :return:
        """
        return [round((fund.allocation_percent / self.accounts[0].equity_percent() * self.account_a_equity_percent_target()), 2) for fund in self.accounts[0].funds]

    def per_fund_bond_increase(self):
        """
        Not working as expected, to be fixed
        :return:
        """
        return [round((fund.allocation_percent / self.accounts[0].bond_percent() * (100 - self.account_a_equity_percent_target())), 2) for fund in self.accounts[0].funds]
