from fastapi import APIRouter, Body
from core.order_operate import (
    place_limit_order,
    place_market_order,
    place_stop_order,
    place_stop_limit_order,
    modify_order,
    cancel_order,
    get_order_status,
)
from core.constant import OrderAction
from utils.data_convert import ApiResponse
from typing import Optional

trading_router = APIRouter(tags=["trading"])


@trading_router.post("/order/limit")
async def create_limit_order(
    symbol: str = Body(..., description="股票代码"),
    quantity: int = Body(..., description="数量"),
    price: float = Body(..., description="限价"),
    action: str = Body(OrderAction.BUY.value, description="交易方向(BUY/SELL)"),
    exchange: str = Body("SMART", description="交易所"),
    currency: str = Body("USD", description="货币"),
    tif: str = Body("DAY", description="订单有效期"),
):
    """创建限价单"""
    try:
        order = place_limit_order(
            symbol=symbol,
            quantity=quantity,
            price=price,
            action=action,
            exchange=exchange,
            currency=currency,
            tif=tif,
        )
        return ApiResponse.success(order)
    except Exception as e:
        return ApiResponse.error(f"创建限价单失败: {str(e)}")


@trading_router.post("/order/market")
async def create_market_order(
    symbol: str = Body(..., description="股票代码"),
    quantity: int = Body(..., description="数量"),
    action: str = Body(OrderAction.BUY.value, description="交易方向(BUY/SELL)"),
    exchange: str = Body("SMART", description="交易所"),
    currency: str = Body("USD", description="货币"),
):
    """创建市价单"""
    try:
        order = place_market_order(
            symbol=symbol,
            quantity=quantity,
            action=action,
            exchange=exchange,
            currency=currency,
        )
        return ApiResponse.success(order)
    except Exception as e:
        return ApiResponse.error(f"创建市价单失败: {str(e)}")


@trading_router.post("/order/stop")
async def create_stop_order(
    symbol: str = Body(..., description="股票代码"),
    quantity: int = Body(..., description="数量"),
    stop_price: float = Body(..., description="止损价"),
    action: str = Body(OrderAction.SELL.value, description="交易方向(BUY/SELL)"),
    exchange: str = Body("SMART", description="交易所"),
    currency: str = Body("USD", description="货币"),
):
    """创建止损单"""
    try:
        order = place_stop_order(
            symbol=symbol,
            quantity=quantity,
            stop_price=stop_price,
            action=action,
            exchange=exchange,
            currency=currency,
        )
        return ApiResponse.success(order)
    except Exception as e:
        return ApiResponse.error(f"创建止损单失败: {str(e)}")


@trading_router.post("/order/stop-limit")
async def create_stop_limit_order(
    symbol: str = Body(..., description="股票代码"),
    quantity: int = Body(..., description="数量"),
    stop_price: float = Body(..., description="止损价"),
    limit_price: float = Body(..., description="限价"),
    action: str = Body(OrderAction.SELL.value, description="交易方向(BUY/SELL)"),
    exchange: str = Body("SMART", description="交易所"),
    currency: str = Body("USD", description="货币"),
):
    """创建止损限价单"""
    try:
        order = place_stop_limit_order(
            symbol=symbol,
            quantity=quantity,
            stop_price=stop_price,
            limit_price=limit_price,
            action=action,
            exchange=exchange,
            currency=currency,
        )
        return ApiResponse.success(order)
    except Exception as e:
        return ApiResponse.error(f"创建止损限价单失败: {str(e)}")


@trading_router.put("/order/{order_id}")
async def update_order(
    order_id: int,
    quantity: Optional[int] = Body(None, description="新数量"),
    price: Optional[float] = Body(None, description="新价格"),
):
    """修改订单"""
    try:
        order = modify_order(
            order_id=order_id,
            new_quantity=quantity,
            new_price=price,
        )
        return ApiResponse.success(order)
    except Exception as e:
        return ApiResponse.error(f"修改订单失败: {str(e)}")


@trading_router.delete("/order/{order_id}")
async def delete_order(order_id: int):
    """取消订单"""
    try:
        result = cancel_order(order_id)
        return ApiResponse.success(result)
    except Exception as e:
        return ApiResponse.error(f"取消订单失败: {str(e)}")


@trading_router.get("/order/{order_id}")
async def get_order(order_id: int):
    """获取订单状态"""
    try:
        order = get_order_status(order_id)
        return ApiResponse.success(order)
    except Exception as e:
        return ApiResponse.error(f"获取订单状态失败: {str(e)}")


@trading_router.get("/orders")
async def get_orders():
    """获取所有订单"""
    try:
        orders = get_order_status()
        return ApiResponse.success(orders)
    except Exception as e:
        return ApiResponse.error(f"获取订单列表失败: {str(e)}")
