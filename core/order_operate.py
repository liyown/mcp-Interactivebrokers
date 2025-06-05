from ib_async import Order, Stock, LimitOrder, MarketOrder, StopOrder, StopLimitOrder
from core.constant import OrderAction, OrderType
from core import ib
from typing import Optional


def place_limit_order(
    symbol: str,
    quantity: int,
    price: float,
    action: str = OrderAction.BUY.value,
    exchange: str = "SMART",
    currency: str = "USD",
    tif: str = "DAY",
):
    """下限价单"""
    order = LimitOrder(action=action, totalQuantity=quantity, lmtPrice=price, tif=tif)
    contract = Stock(symbol, exchange, currency)
    trade = ib.placeOrder(contract, order)
    if trade:
        return format_order_response(trade)
    return None


def place_market_order(
    symbol: str,
    quantity: int,
    action: str = OrderAction.BUY.value,
    exchange: str = "SMART",
    currency: str = "USD",
):
    """下市价单"""
    order = MarketOrder(
        action=action,
        totalQuantity=quantity,
    )
    contract = Stock(symbol, exchange, currency)
    trade = ib.placeOrder(contract, order)
    if trade:
        return format_order_response(trade)
    return None


def place_stop_order(
    symbol: str,
    quantity: int,
    stop_price: float,
    action: str = OrderAction.SELL.value,
    exchange: str = "SMART",
    currency: str = "USD",
):
    """下止损单"""
    order = StopOrder(
        action=action,
        totalQuantity=quantity,
        stopPrice=stop_price,
    )
    contract = Stock(symbol, exchange, currency)
    trade = ib.placeOrder(contract, order)
    if trade:
        return format_order_response(trade)
    return None


def place_stop_limit_order(
    symbol: str,
    quantity: int,
    stop_price: float,
    limit_price: float,
    action: str = OrderAction.SELL.value,
    exchange: str = "SMART",
    currency: str = "USD",
):
    """下止损限价单"""
    order = StopLimitOrder(
        action=action,
        totalQuantity=quantity,
        stopPrice=stop_price,
        lmtPrice=limit_price,
    )
    contract = Stock(symbol, exchange, currency)
    trade = ib.placeOrder(contract, order)
    if trade:
        return format_order_response(trade)
    return None


def modify_order(
    order_id: int,
    new_quantity: Optional[int] = None,
    new_price: Optional[float] = None,
):
    """修改订单"""
    trades = ib.trades()
    for trade in trades:
        if trade.order.orderId == order_id:
            # 创建新订单，保持原有参数
            new_order = trade.order
            if new_quantity is not None:
                new_order.totalQuantity = new_quantity
            if new_price is not None:
                if new_order.orderType == OrderType.LIMIT.value:
                    new_order.lmtPrice = new_price
                elif new_order.orderType in [
                    OrderType.STOP.value,
                    OrderType.STOP_LIMIT.value,
                ]:
                    new_order.stopPrice = new_price

            # 取消原订单并提交新订单
            ib.cancelOrder(trade.order)
            modified_trade = ib.placeOrder(trade.contract, new_order)
            if modified_trade:
                return format_order_response(modified_trade)
    return None


def cancel_order(order_id: int):
    """取消订单"""
    order = Order()
    order.orderId = order_id
    ib.cancelOrder(order)
    return f"""<cancelOrder>
        <orderId>
            <value>{order_id}</value>
            <description>ID of the cancelled order</description>
        </orderId>
    </cancelOrder>"""


def get_order_status(order_id: Optional[int] = None):
    """获取订单状态"""
    trades = ib.trades()
    if order_id is None:
        return [format_order_response(trade) for trade in trades]
    else:
        for trade in trades:
            if trade.order.orderId == order_id:
                return format_order_response(trade)
    return None


def format_order_response(trade):
    """格式化订单响应"""
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
            <value>{getattr(trade.order, "lmtPrice", None) or getattr(trade.order, "stopPrice", None)}</value>
            <description>Order price</description>
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
        <lastFillTime>
            <value>{trade.orderStatus.lastFillTime}</value>
            <description>Last fill time</description>
        </lastFillTime>
        <whyHeld>
            <value>{trade.orderStatus.whyHeld}</value>
            <description>Why order is held</description>
        </whyHeld>
    </orderStatus>"""
