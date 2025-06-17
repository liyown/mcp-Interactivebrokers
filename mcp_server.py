# 创建 MCP 实例
from fastmcp import FastMCP
from core.info_operate import get_portfolio, get_pnl, get_account_summary
from core.order_operate import (
    place_limit_order,
    place_market_order,
    cancel_order,
    get_order_status,
)
from core.websocket import websocket_manager
from core.market_data_operate import get_stock_quote, get_historical_data

mcp = FastMCP(
    name="trading",
    instructions="You are a stock trader, please trade according to the user's needs.",
)
mcp_app = mcp.http_app(path="/sse", transport="sse")


@mcp.tool()
async def get_account_portfolio() -> str:
    """Get account portfolio information"""
    return get_portfolio()


@mcp.tool()
async def get_account_pnl() -> str:
    """Get account profit and loss information"""
    return get_pnl()


@mcp.tool()
async def get_account_details() -> str:
    """Get detailed account information"""
    return get_account_summary()


@mcp.tool()
async def create_limit_order(symbol: str, quantity: int, price: float) -> str:
    """
    Create a limit order
    Args:
        symbol: Stock symbol
        quantity: Order quantity
        price: Limit price
    """
    formatted_order, trade = await place_limit_order(symbol, quantity, price)

    # 发送MCP创建订单的WebSocket通知
    if trade:
        await _send_mcp_order_notification(trade, "MCP创建限价单")

    return formatted_order


@mcp.tool()
async def request_stock_quote(symbol: str) -> str:
    """
    Request quote
    Args:
        symbol: Stock symbol
    """
    quote, _ = await get_stock_quote(symbol)
    return quote


@mcp.tool()
async def request_historical_data(symbol: str, duration: str, bar_size: str) -> str:
    """
    Request historical data
    Args:
        duration: Duration of the data
        bar_size: Size of the bars
    """
    formatted_data, _ = await get_historical_data(symbol, duration, bar_size)

    return formatted_data


@mcp.tool()
async def create_market_order(symbol: str, quantity: int) -> str:
    """
    Create a market order
    Args:
        symbol: Stock symbol
        quantity: Order quantity
    """
    formatted_order, trade = await place_market_order(symbol, quantity)

    # 发送MCP创建订单的WebSocket通知
    if trade:
        await _send_mcp_order_notification(trade, "MCP创建市价单")

    return formatted_order


@mcp.tool()
async def cancel_existing_order(order_id: int) -> str:
    """
    Cancel an existing order
    Args:
        order_id: Order ID to cancel
    """
    result = await cancel_order(order_id)

    # 发送MCP取消订单的WebSocket通知
    await _send_mcp_cancel_notification(order_id)

    return result


@mcp.tool()
async def check_order_status(order_id: int = None) -> str:
    """
    Check order status
    Args:
        order_id: Order ID (optional)
    """
    return await get_order_status(order_id)


async def _send_mcp_order_notification(trade, action: str):
    """发送MCP订单操作的WebSocket通知"""
    await websocket_manager.broadcast(
        {
            "type": "mcp_order",
            "action": action,
            "data": {
                "order_id": trade.order.orderId,
                "symbol": trade.contract.symbol,
                "action": trade.order.action,
                "quantity": trade.order.totalQuantity,
                "order_type": trade.order.orderType,
                "price": (
                    getattr(trade.order, "lmtPrice", None)
                    or getattr(trade.order, "stopPrice", None)
                ),
                "status": trade.orderStatus.status,
            },
            "source": "MCP",
            "message": f"MCP {action}",
            "timestamp": __import__("datetime").datetime.now().isoformat(),
        },
        "mcp_order",
    )


async def _send_mcp_cancel_notification(order_id: int):
    """发送MCP取消订单的WebSocket通知"""
    await websocket_manager.broadcast(
        {
            "type": "mcp_order",
            "action": "MCP取消订单",
            "data": {"order_id": order_id},
            "source": "MCP",
            "message": f"MCP取消订单 {order_id}",
            "timestamp": __import__("datetime").datetime.now().isoformat(),
        },
        "mcp_order",
    )
