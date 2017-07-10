import re
import pandas as pd
import math


def preprocess(text):
    '''Get only Captial Letters from the text'''
    caps = re.findall(r"[A-Z][a-z]+", text)
    caps = [word for word in caps if len(word) > 2]
    text = " ".join(caps)
    text = text.strip()
    return text


def get_english(ls):
    '''Get Only Englis Words'''
    all = [x for x in ls if len(re.findall("[A-Za-z ]*", x)) == 2]
    return all


def get_total_regions(alpha=0.8, infile="database.json"):
    df = pd.DataFrame(pd.read_json(infile))
    regions = df["region"]

    regions = [x[:math.ceil(alpha * len(x))] for x in regions if x is not None]

    ls = []
    for x in regions:
        ls += x

    return "|".join(get_english(ls)) + "|"


def search_core(text, string, alpha=0.8):
    '''Search through the text for max two words'''
    text = preprocess(text)
    res = []

    ls = text.split(" ")
    i = 0
    while True:
        if i >= len(ls):
            break

        if i <= len(ls) - 2:

            two_combined = " ".join([ls[i], ls[i + 1]])
            st = two_combined + "|"
            if st in string:
                res.append(two_combined)
                i += 2

                continue

        st = ls[i] + "|"
        if st in string:
            res.append(ls[i])

        i += 1

    return res


def search_locations(text, alpha=0.8):
    total_string = get_total_regions(alpha=alpha)
    return search_core(text, total_string, alpha)


def search_countries(text):
    with open("countries.txt", 'r') as f:
        countries_ls = f.read()
    countries_ls = "|".join(countries_ls.split("\n"))

    return search_core(text, countries_ls, alpha=1)


def search_nationalities(text):
    with open("nationalities.txt", 'r') as f:
        nationalities = f.read()
        nationalities = "|".join(nationalities.split("\n"))
    text = preprocess(text).split(" ")

    return [word for word in text if word in nationalities]


class geoSearch(object):
    def __init__(self, text, alpha=0.8):
        self.locations = search_locations(text, alpha)
        self.countries = search_countries(text)
        self.nationalities = search_nationalities(text)