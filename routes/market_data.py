from fastapi import APIRouter, Query
from core.market_data_operate import (
    get_stock_quote,
    get_historical_data,
    get_option_chain,
)
from utils.data_convert import ApiResponse

market_data_router = APIRouter(tags=["market_data"])


@market_data_router.get("/quote/{symbol}")
async def get_quote(
    symbol: str,
    exchange: str = Query(default="SMART", description="交易所代码"),
    currency: str = Query(default="USD", description="货币代码"),
):
    """获取股票实时报价"""
    try:
        _, quote = get_stock_quote(symbol, exchange, currency)
        return ApiResponse.success(quote)
    except Exception as e:
        return ApiResponse.error(f"获取报价失败: {str(e)}")


@market_data_router.get("/history/{symbol}")
async def get_history(
    symbol: str,
    duration: str = Query(default="1 D", description="数据时长，如 1 D, 1 W, 1 M, 1 Y"),
    bar_size: str = Query(
        default="1 min", description="K线周期，如 1 min, 5 mins, 1 hour, 1 day"
    ),
    exchange: str = Query(default="SMART", description="交易所代码"),
    currency: str = Query(default="USD", description="货币代码"),
):
    """获取历史数据"""
    try:
        _, raw_bars = await get_historical_data(
            symbol,
            duration=duration,
            bar_size=bar_size,
            exchange=exchange,
            currency=currency,
        )
        return ApiResponse.success(raw_bars)
    except Exception as e:
        return ApiResponse.error(f"获取历史数据失败: {str(e)}")


@market_data_router.get("/options/{symbol}")
async def get_options(
    symbol: str,
    exchange: str = Query(default="SMART", description="交易所代码"),
    currency: str = Query(default="USD", description="货币代码"),
):
    """获取期权链数据"""
    try:
        _, chains = await get_option_chain(symbol, exchange, currency)
        return ApiResponse.success(chains)
    except Exception as e:
        return ApiResponse.error(f"获取期权链数据失败: {str(e)}")
