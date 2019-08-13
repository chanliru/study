from ib_insync import *
# util.startLoop()
 
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)
 
 
contract = Stock('AAPL', 'SMART', 'USD')
ib.qualifyContracts(contract)
 
order = MarketOrder('BUY', 1)
 
trade = ib.placeOrder(contract, order)
 
print(trade)
 
ib.sleep(1)
print(trade.log)
 
limitOrder = LimitOrder('BUY', 1, 0.05)
limitTrade = ib.placeOrder(contract, limitOrder)
 
print(limitTrade)
 
ib.cancelOrder(limitOrder)

