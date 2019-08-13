import pandas as pd
from ib_insync import *
# util.startLoop()  # uncomment this line when in a notebook
 
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)
 
 
code = "PDD"
 
contract = Stock(code, exchange="SMART")
bars = ib.reqHistoricalData(contract, endDateTime='20190314 18:30:00', durationStr='1 D',
        barSizeSetting='30 secs', whatToShow='MIDPOINT', useRTH=True)
 
# convert to pandas dataframe:
df = util.df(bars)
print(df[['date', 'open', 'high', 'low', 'close']])
