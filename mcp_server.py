# 创建 MCP 实例
from fastmcp import FastMCP
from core.info_operate import get_portfolio, get_pnl, get_account_summary
from core.order_operate import (
    place_limit_order,
    place_market_order,
    cancel_order,
    get_order_status,
)

mcp = FastMCP(
    name="trading",
    instructions="You are a stock trader, please trade according to the user's needs.",
)
mcp_app = mcp.http_app(path="/sse", transport="sse")


@mcp.tool()
def get_account_portfolio() -> str:
    """Get account portfolio information"""
    return get_portfolio()


@mcp.tool()
def get_account_pnl() -> str:
    """Get account profit and loss information"""
    return get_pnl()


@mcp.tool()
def get_account_details() -> str:
    """Get detailed account information"""
    return get_account_summary()


@mcp.tool()
def create_limit_order(symbol: str, quantity: int, price: float) -> str:
    """
    Create a limit order
    Args:
        symbol: Stock symbol
        quantity: Order quantity
        price: Limit price
    """
    return place_limit_order(symbol, quantity, price)


@mcp.tool()
def create_market_order(symbol: str, quantity: int) -> str:
    """
    Create a market order
    Args:
        symbol: Stock symbol
        quantity: Order quantity
    """
    return place_market_order(symbol, quantity)


@mcp.tool()
def cancel_existing_order(order_id: int) -> str:
    """
    Cancel an existing order
    Args:
        order_id: Order ID to cancel
    """
    return cancel_order(order_id)


@mcp.tool()
def check_order_status(order_id: int = None) -> str:
    """
    Check order status
    Args:
        order_id: Order ID (optional)
    """
    return get_order_status(order_id)
