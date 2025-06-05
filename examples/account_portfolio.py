# /// script
# requires-python = ">=3.13"
# dependencies = ["ib_async"]
# ///

from ib_async import IB, Stock, MarketOrder


ib = IB()
ib.connect("127.0.0.1", 7497, clientId=2)

print(ib.accountValues())


# contract = Stock("AAPL", "SMART", "USD")
# order = MarketOrder("BUY", 1000)
# ib.placeOrder(contract, order)
