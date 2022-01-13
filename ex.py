import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

wiki_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

yahoo_url = "https://finance.yahoo.com/quote/AAPL?p=AAPL"

# get tickers from wiki site
wiki_res = requests.get(wiki_url)
wiki_res_txt = wiki_res.text
wiki_soup = BeautifulSoup(wiki_res_txt, features='html.parser')
wiki_table = wiki_soup.find("table", {"id": "constituents"})
wiki_tr_tags = wiki_table.find_all("tr")

tickers = []
for tr_tag in wiki_tr_tags[1:]:
    tickers.append(tr_tag.contents[1].text.split('\n')[0])

# print(len(tickers))
# print(tickers)

# wait for 1 second
time.sleep(1)
data = []
# get additional info from yahoo finance site
for ticker in tickers:
    tickerObj = {"ticker": ticker}
    try:
        yahoo_url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}"
        yahoo_res = requests.get(yahoo_url)
        yahoo_res_txt = yahoo_res.text
        yahoo_soup = BeautifulSoup(yahoo_res_txt, features='html.parser')
        yahoo_tables = yahoo_soup.find_all("table")
        yahoo_table_cells = yahoo_tables[0].find_all(
            'td') + yahoo_tables[1].find_all('td')

        for idx in range(len(yahoo_table_cells)):
            if idx % 2 == 0:
                name = yahoo_table_cells[idx].text
            else:
                value = yahoo_table_cells[idx].text
                tickerObj[name] = value
        data.append(tickerObj)
    except:
        continue

df = pd.DataFrame(data)
df.to_csv('SP500.csv', index=False)
