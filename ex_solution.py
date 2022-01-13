import requests
from bs4 import BeautifulSoup


def getFinancialInformation():
    url = "https://finance.yahoo.com/quote/AAPL?p=AAPL"

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
