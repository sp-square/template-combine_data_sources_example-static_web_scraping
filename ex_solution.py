import requests
from bs4 import BeautifulSoup
import pandas as pd


def getFinancialInformation(symbol):
    url = "https://finance.yahoo.com/quote/"+symbol+"?p="+symbol

    response = requests.get(url)
    response_text = response.text

    soup = BeautifulSoup(response_text, features='html.parser')
    final_name = '1y Target Est'
    tr_tags = soup.find_all('tr')

    names = []
    values = []

    name_values = {}

    for i in range(len(tr_tags)):
        for j in range(len(tr_tags[i].contents)):
            if j == 0:
                try:
                    name = tr_tags[i].contents[j].text
                    names.append(name)
                except:
                    names.append('')
                    continue
            if j == 1:
                try:
                    value = tr_tags[i].contents[j].text
                    values.append(value)
                except:
                    values.append('')
                    continue
        name_values[name] = value
        if name == final_name:
            break

    return names, values


def getCompanyList():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    res = requests.get(url)
    res_txt = res.text
    soup = BeautifulSoup(res_txt, features='html.parser')

    tbody = soup.find_all("tbody")

    tickerSymbols = []
    for i in range(len(tbody[0].contents)):
        if i < 2 or i % 2 != 0:
            continue
        ticker = tbody[0].contents[i].contents[1].text
        tickerSymbols.append(ticker.strip('\n'))

    return tickerSymbols


data = {"symbol": [], "metric": [], "value": []}
tickerSymbols = getCompanyList()

for symbol in tickerSymbols:
    names, values = getFinancialInformation(symbol)
    for i in range(len(names)):
        data["symbol"].append(symbol)
        data["metric"].append(names[i])
        data["value"].append(values[i])
    # another way to collect the data would be as follows:
    # data["symbol"] += [symbol] * len(names)
    # data["metric"] += names
    # data["value"] += values

df = pd.DataFrame(data)
df.to_csv("financialData.csv")
