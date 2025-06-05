from ib_async import Order, Stock, LimitOrder, MarketOrder
from core.constant import OrderAction
from core import ib


def place_limit_order(symbol: str, quantity: int, price: float):
    order = LimitOrder(OrderAction.BUY.value, quantity, price)
    contract = Stock(symbol, "SMART", "USD")
    trade = ib.placeOrder(contract, order)
    format_result = None
    if trade:
        format_result = f"""<order>
            <orderId>
                <value>{trade.order.orderId}</value>
                <description>Order ID</description>
            </orderId>
        </order>"""
    return format_result


def place_market_order(symbol: str, quantity: int):
    order = MarketOrder(OrderAction.BUY.value, quantity)
    contract = Stock(symbol, "SMART", "USD")
    trade = ib.placeOrder(contract, order)
    format_result = None
    if trade:
        format_result = f"""<order>
            <orderId>
                <value>{trade.order.orderId}</value>
                <description>Order ID</description>
            </orderId>
        </order>"""
    return format_result


def cancel_order(order_id: int):
    order = Order(order_id)
    ib.cancelOrder(order)
    return f"""<cancelOrder>
        <orderId>
            <value>{order_id}</value>
            <description>ID of the cancelled order</description>
        </orderId>
    </cancelOrder>"""


def get_order_status(order_id: int = None):
    trades = ib.trades()
    if order_id is None:
        return [get_order_status(trade.order.orderId) for trade in trades]
    else:
        for trade in trades:
            if trade.order.orderId == order_id:
                return f"""<orderStatus>
                    <orderId>
                        <value>{trade.order.orderId}</value>
                        <description>Order ID</description>
                    </orderId>
                    <symbol>
                        <value>{trade.contract.symbol}</value>
                        <description>Stock symbol</description>
                    </symbol>
                    <type>
                        <value>{trade.order.orderType}</value>
                        <description>Order type</description>
                    </type>
                    <action>
                        <value>{trade.order.action}</value>
                        <description>Buy/Sell action</description>
                    </action>
                    <quantity>
                        <value>{trade.order.totalQuantity}</value>
                        <description>Order quantity</description>
                    </quantity>
                    <price>
                        <value>{trade.order.lmtPrice}</value>
                        <description>Limit price</description>
                    </price>
                    <status>
                        <value>{trade.orderStatus.status}</value>
                        <description>Order status</description>
                    </status>
                    <filled>
                        <value>{trade.filled()}</value>
                        <description>Filled quantity</description>
                    </filled>
                    <remaining>
                        <value>{trade.remaining()}</value>
                        <description>Remaining quantity</description>
                    </remaining>
                    <avgFillPrice>
                        <value>{trade.orderStatus.avgFillPrice}</value>
                        <description>Average fill price</description>
                    </avgFillPrice>
                </orderStatus>"""
    return None
