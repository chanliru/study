import requests
import pandas
import datetime
import io
import os

def dataframeFromUrl(url):
	dataString = requests.get(url).content
	parsedResult = pandas.read_csv(io.StringIO(dataString.decode('utf-8')),index_col=0)
	return parsedResult
def stockPriceIntraday(ticker,folder):
	url = 'https://www.alphavantage.co/query?apikey=NSPPU6PM4SMNSA5B&function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=1min&outputsize=full&datatype=csv'.format(ticker=ticker)
	intraday = dataframeFromUrl(url)
	file = folder+'/'+ticker+'.csv'
	if os.path.exists(file):
		history = pandas.read_csv(file,index_col=0)
		intraday.append(history)
	intraday.sort_index(inplace=True)
	intraday.to_csv(file)
	print('intraday for['+ticker+']got.')



#1,get ticker list online
url = 'https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download'
dataString = requests.get(url).content
tickersRawData = pandas.read_csv(io.StringIO(dataString.decode('utf-8')))
tickers = tickersRawData['Symbol'].tolist()


#2,save the tickerlist to a local file
dateToday = datetime.datetime.today().strftime('%Y%m%d')
file = '../02. Data/00. TickerListUS/TickerList_'+dateToday+'.csv'
tickersRawData.to_csv(file,index=False)
print('Tickers saved.')
#3,Get stock price
'''for i,ticker in enumerate(tickers):
	try:
		print('Intraday',i,'',len(tickers))'''

stockPriceIntraday('QQQ', folder='../02. Data/01. IntradayUS')
'''time.sleep(3)
	except:
		pass
	if i>5:
		break'''

print('over')







