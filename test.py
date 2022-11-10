import pandas as pd

tickersSeries = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol']
tickersList = tickersSeries.to_list()


print(tickersList)