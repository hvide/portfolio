from helpers import yml_load, jinja2_load
from pprint import pprint
import pandas as pd

class Account:
    def __init__(self, provider, value, funds=[]):
        self.provider = provider
        self.value = value
        self.funds = funds

    def tot_actual_ofc(self):
        """
        Calculate OFC of the overall account by summing the actual_ofc together
        :return:
        """
        x = [fund.actual_ofc() for fund in self.funds]
        return sum(x)

    def tot_actual_ofc_value(self, value):
        """
        Calculate Total of the actual OFC in £ by summing actual_ofc_value together
        :param value: Total value of the account in £
        :return:
        """
        x = [fund.actual_ofc_value(value) for fund in self.funds]
        return sum(x)

class Fund:
    def __init__(self, isin, name, nav, ofc, fund_type, allocation_percent):
        self.isin = isin
        self.name = name
        self.nav = nav
        self.ofc = ofc
        self.fund_type = fund_type
        self.allocation_percent = allocation_percent

    def allocation_value(self, value):
        return (self.allocation_percent / 100) * value

    def ofc_percent(self):
        return self.ofc * 100

    def actual_ofc(self):
        return (self.allocation_percent / 100) * self.ofc

    def actual_ofc_value(self, value):
        return (self.allocation_value(value) / 100) * self.ofc

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


def main():

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)

    funds_info_yml = yml_load('funds_info.yml')
    portfolios_yml = yml_load('portfolios.yml')


    for portfolio, acc in portfolios_yml.items():
    # for portfolio in portfolios_yml['portfolios']:
        print('########################')
        print(portfolio)
        for p, funds in acc.items():
            portfolio_list = []
            # test = portfolios_yml[p]
            # print("Account name: %s" % p)
            for fund in funds[1]:
                # print(p)
                # print(funds[fund])
                fund_obj = Fund(isin=fund,
                                name=funds_info_yml[fund]['name'],
                                nav=funds_info_yml[fund]['nav'],
                                ofc=funds_info_yml[fund]['ofc'],
                                fund_type=funds_info_yml[fund]['fund_type'],
                                allocation_percent=funds[1][fund])
                portfolio_list.append(fund_obj)

                # print(fund.__dict__)
                # print(fund.allocation_value(portfolios_yml['value']))
                # print(fund.ofc_percent())
                # print(fund.actual_ofc())
                # print(fund.actual_ofc_value(portfolios_yml['value']))
            account_value = funds[0]['value']
            account = Account(p, account_value, portfolio_list)

            df = pd.DataFrame([p.to_dict(account_value) for p in portfolio_list])
            print("Account name: %s" % account.provider)
            print("Account value: £%s" % account.value)
            print("tot_actual_ofc: %s" % account.tot_actual_ofc())
            print("tot_actual_ofc_value: %s" % account.tot_actual_ofc_value(account_value))
            print(df)
            print('')
        print('')


if __name__ == '__main__':
    main()


