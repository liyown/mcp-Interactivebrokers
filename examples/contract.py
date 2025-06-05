from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import time
import threading

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId):
        self.orderId = orderId

    def nextId(self):
        self.orderId += 1
        return self.orderId
    
    def currentTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=""):
        print(f"reqId: {reqId}, errorCode: {errorCode}, errorString: {errorString}, advancedOrderRejectJson: {advancedOrderRejectJson}")

    def contractDetails(self, reqId, contractDetails):
        attrs = vars(contractDetails)
        for attr in attrs:
            print(f"{attr}: {attrs[attr]}")


    def contractDetailsEnd(self, reqId):
        print(f"reqId: {reqId}, contractDetailsEnd")
        self.disconnect()

if __name__ == "__main__":
    app = TestApp()
    app.connect("127.0.0.1", 7497, 0)
    thread = threading.Thread(target=app.run).start()
    time.sleep(1)
    

    my_contract = Contract()

    # 股票
    my_contract.symbol = "AAPL"
    my_contract.secType = "STK"
    my_contract.currency = "USD"
    my_contract.exchange = "SMART"
    my_contract.primaryExchange = "NASDAQ"
    app.reqContractDetails(app.nextId(), my_contract)
        
            
