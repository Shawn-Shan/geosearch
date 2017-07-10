from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd
import time


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('%r  %2.2f sec' % \
              (method.__name__, te - ts))
        return result

    return timed


def next_page(url):
    '''Given the url of a geonames.org page, find the next page.
    If the total exceed 5000, the function will stop, because geonames.org does not support search over 5000'''

    geonames = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(geonames, "lxml")
    soup = soup.find("div", id="search")
    link = soup.find_all('a', href=True)
    next_or_pre = link[-1].getText()

    if "next >" != next_or_pre:
        return

    innerlink = link[-1]["href"]

    '''extract the startrow of the next page'''

    start_page = re.search(r"startRow=(.*?)$", innerlink)
    if start_page is None:
        print("This is the last page")
        return

    start_page = innerlink[start_page.start() + 9: start_page.end()]
    if int(start_page) > 5000:
        print("Searching Exceed 5000")
        return
    print(innerlink)
    link = "http://www.geonames.org" + innerlink + "&maxRows=500"

    return link


@timeit
def get_page(url):
    '''Given the url of a geonames.org page, parse the data from the webpage'''

    country = []
    geonames = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(geonames, "lxml")
    soup = soup.find("div", id="search")
    countries = soup.find_all("table", class_="restable")
    table = countries[1].find_all("tr")

    for rows in table:
        try:
            cur_name = rows.find_all("td")[1]

            cur_feature = rows.find_all("td")[3]
        except IndexError:
            continue
        if cur_name is None or cur_feature is None:
            continue
        cur_name_ls = cur_name.find_all("a", href=True)

        cur_name = cur_name_ls[0]
        if len(cur_name_ls) == 1:
            cur_wiki_link = None
        else:
            cur_wiki_link = cur_name_ls[1]

        if cur_name is None:
            cur_name = "None"
        else:
            cur_name = cur_name.getText()

        if cur_wiki_link is None:
            cur_wiki_link = "None"
        else:
            cur_wiki_link = cur_wiki_link["href"]
            if "http://en.wikipedia.org/wiki/" not in cur_wiki_link:
                cur_wiki_link = "None"

        cur_feature = cur_feature.getText()
        cur_feature = re.split("population|elevation", cur_feature)[0]

        country.append([cur_name, cur_wiki_link, cur_feature])

    return country


def get_country(country_name):
    '''Get top 5000 place for each country'''

    country_ls = []
    if not isinstance(country_name, str):
        country_name = "NA"

    url = "http://www.geonames.org/advanced-search.html?q=&featureClass=A&startRow=0&maxRows=500&country=" + country_name

    nextpage = url

    while True:
        country_ls += get_page(nextpage)
        print(0)
        nextpage = next_page(nextpage)

        if nextpage is None:
            break
    region = []
    wiki_link = []
    feature = []
    for x in country_ls:
        region.append(x[0])
        wiki_link.append(x[1])
        feature.append(x[2])

    return [country_name, region, wiki_link, feature]


def get_all_countries():
    df_country = pd.DataFrame(pd.read_csv("all_countries.csv"))
    countries = df_country["abb"]
    total_ls = []

    for country in countries:
        print(country)
        if not isinstance(country, str):
            print(country)

        total_ls.append(get_country(country))

    df = pd.DataFrame(total_ls, columns=["country", "region", "wiki_link", "category"])

    df.to_csv("database.csv")

    df.to_json("database.json")


get_all_countries()

def get_index(ls, ele):
    for i in range(0, len(ls)):
        if ele == ls[i]:
            return i
    return
