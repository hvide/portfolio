import requests
from bs4 import BeautifulSoup
from utils import yml_load, jinja2_load
from pprint import pprint

conf_yml = yml_load('templates/urls.yml')
funds = conf_yml['funds']
# urls = ['https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id=F000003YD7']
fund_info_j2 = jinja2_load('templates/fund.j2')
fund_list = []

for fund in funds:
    r = requests.get(fund['url'])
    c = r.content

    soup = BeautifulSoup(c, "html.parser")
    # print(soup.prettify())

    title = soup.find_all("div", {"class": "snapshotTitleBox"})[
        0].select('h1')[0].text.splitlines()[0]
    # print(title)
    # if '\n' in title:
    #     title = title.split('\n', 0)
    info = soup.find_all("table", {"class": "snapshotTextColor snapshotTextFontStyle snapshotTable overviewKeyStatsTable"})[
        0].find_all("td", {"class": "line text"})
    # nav = info[0].text
    if fund['url'].split('/')[4] == 'funds':
        isin = info[3].text
        nav = info[0].text.split()[1]
    elif fund['url'].split('/')[4] == 'etf':
        isin = info[4].text
        nav = info[0].text.split()[1]
    ofc = info[7].text[:-1]
    data = {
        'isin': isin,
        'title': title,
        'nav': nav,
        'ofc': ofc,
        'fund_type': fund['fund_type']
    }
    fund_list.append(data)
    print(fund_info_j2.render(data))
