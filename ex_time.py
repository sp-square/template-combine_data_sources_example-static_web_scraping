import requests
import time
import datetime
import os
import pandas as pd
from bs4 import BeautifulSoup


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


while True:
    # decide how often you want the program to run
    waitTime = 150  # for example run every 150 seconds
    # collect the current time
    startTime = time.time()

    # extract and save data
    data = {"symbol": [], "metric": [], "value": [], "time": []}

    try:
        tickerSymbols = getCompanyList()
    except Exception as e:
        print(str(e))
        time.sleep(60)
        continue

    for symbol in tickerSymbols:
        try:
            names, values = getFinancialInformation(symbol)
        except Exception as e:
            print(str(e))
            continue

        collectedTime = datetime.datetime.now().timestamp()

        for i in range(len(names)):
            data["symbol"].append(symbol)
            data["metric"].append(names[i])
            data["value"].append(values[i])
            data["time"].append(collectedTime)

    currentDate = datetime.date.today()
    df = pd.DataFrame(data)
    # have a csv file created for every single day
    savedFilename = f"{str(currentDate)}-financial-data.csv"
    # check if file already exists
    if os.path.isfile(savedFilename):
        # don't overwrite file, rather append to it (mode="a")
        df.to_csv(savedFilename, mode="a", header=False,  columns=[
                  "symbol", "metric", "value", "time"])  # ensure columns are saved in same order every time
    else:
        # create file
        df.to_csv(savedFilename, columns=["symbol", "metric", "value", "time"])

    # wait until 15 s have passed from above
    timeDiff = time.time() - startTime
    if waitTime - timeDiff > 0:
        time.sleep(waitTime - timeDiff)
