from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import time
import threading

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId):
        self.orderId = orderId
        print("NextValidId: ", orderId)

    def nextOrderId(self):
        self.orderId += 1
        return self.orderId

    def nextId(self):
        self.orderId += 1
        return self.orderId
    
    def currentTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=""):
        print(f"reqId: {reqId}, errorCode: {errorCode}, errorString: {errorString}, advancedOrderRejectJson: {advancedOrderRejectJson}")

    
        

if __name__ == "__main__":
    app = TestApp()
    app.connect("127.0.0.1", 7497, 0)
    thread = threading.Thread(target=app.run).start()
    time.sleep(1)
    

    for i in range(10):
        print(app.nextId())
        
            
