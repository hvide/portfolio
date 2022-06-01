import requests
from bs4 import BeautifulSoup
# from utils import yml_load, jinja2_load
# from pprint import pprint

# conf_yml = yml_load('app/scraper/conf.yml')
# urls = conf_yml['urls']
# fund_info_j2 = jinja2_load('app/scraper/fund_info.j2')
# fund_list = []


def get_info_bulk():
    for url in urls:
        r = requests.get(url)
        c = r.content

        soup = BeautifulSoup(c, "html.parser")
        # print(soup.prettify())

        title = soup.find_all("div", {"class": "snapshotTitleBox"})[
            0].select('h1')[0].text.splitlines()[0]

        info = soup.find_all("table", {"class": "snapshotTextColor snapshotTextFontStyle snapshotTable overviewKeyStatsTable"})[
            0].find_all("td", {"class": "line text"})

        if url.split('/')[4] == 'funds':
            isin = info[3].text
            nav = info[0].text.split()[1]

        elif url.split('/')[4] == 'etf':
            isin = info[4].text
            nav = info[0].text.split()[1]

        ofc = info[7].text[:-1]

        fund = {
            'isin': isin,
            'title': title,
            'nav': nav,
            'ofc': ofc,
            'url': url,
        }

        fund_list.append(fund)

    return fund_list


def get_info(url):

    r = requests.get(url)
    c = r.content

    soup = BeautifulSoup(c, "html.parser")
    # print(soup.prettify())

    title = soup.find_all("div", {"class": "snapshotTitleBox"})[
        0].select('h1')[0].text.splitlines()[0]

    info = soup.find_all("table", {"class": "snapshotTextColor snapshotTextFontStyle snapshotTable overviewKeyStatsTable"})[
        0].find_all("td", {"class": "line text"})

    if url.split('/')[4] == 'funds':
        isin = info[3].text
        nav = info[0].text.split()[1]

    elif url.split('/')[4] == 'etf':
        isin = info[4].text
        nav = info[0].text.split()[1]

    ofc = info[7].text[:-1]

    fund = {
        # 'isin': isin,
        # 'title': title,
        'nav': nav,
        'ofc': ofc,
        # 'url': url,
    }

    return fund
