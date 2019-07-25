import requests
import pandas
import io
import datetime

#1,get ticker list online
url = 'https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download'
dataString = requests.get(url).content
tickersRawData = pandas.read_csv(io.StringIO(dataString.decode('utf-8')))
tickers = tickersRawData['Symbol'].tolist()
print(tickers)


#2,save the tickerlist to a local file
dateToday = datetime.datetime.today().strftime('%Y%m%d')
file = '../02. Data/00. TickerListUS/TickerList_'+dateToday+'.csv'
tickersRawData.to_csv(file,index=False)
print('Tickers saved.')



