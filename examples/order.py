from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import time
import threading

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId):
        
        my_contract = Contract()
        my_contract.symbol = "AAPL"
        my_contract.secType = "STK"
        my_contract.currency = "USD"
        my_contract.exchange = "SMART"
        my_contract.primaryExchange = "NASDAQ"
        self.reqContractDetails(orderId, my_contract)
    
    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=""):
        print(f"reqId: {reqId}, errorCode: {errorCode}, errorString: {errorString}, advancedOrderRejectJson: {advancedOrderRejectJson}")

    def contractDetails(self, reqId, contractDetails):
        print(f"reqId: {reqId}, contractDetails' contract: {contractDetails.contract}")

        my_contract = contractDetails.contract

        my_order = Order()
        my_order.orderId = reqId
        my_order.action = "BUY"
        my_order.tif = "GTC"
        my_order.totalQuantity = 10
        my_order.orderType = "LMT"
        my_order.lmtPrice = 100
        self.placeOrder(reqId, my_contract, my_order)
        self.cancelOrder(reqId)

    def openOrder(self, orderId, contract, order, status):
        print(f"orderId: {orderId}, contract: {contract}, order: {order}, status: {status}")

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print(f"orderId: {orderId}, status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}, clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")    

    def execDetails(self, reqId, execution):
        print(f"reqId: {reqId}, execution: {execution}")



if __name__ == "__main__":
    app = TestApp()
    app.connect("127.0.0.1", 7497, 0)
    app.run()

        
            
