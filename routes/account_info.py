import asyncio
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from core import ib
from core.config import get_settings
from utils.data_convert import format_account_summary, ApiResponse
from typing import AsyncGenerator

account_info_router = APIRouter(tags=["account_info"])


@account_info_router.get("/account_summary")
async def get_account_summary():
    account_summary = ib.accountValues()
    formatted_account_summary = format_account_summary(account_summary)
    return formatted_account_summary


async def get_account_status(request: Request) -> AsyncGenerator[str, None]:
    while True:
        account_status = ib.isConnected()
        yield ApiResponse.success(
            {
                "status": account_status,
                "message": "connected" if account_status else "disconnected",
            }
        ).sse_encode()
        await asyncio.sleep(5)


@account_info_router.get("/account_status")
async def account_status(request: Request):
    return StreamingResponse(
        get_account_status(request), media_type="text/event-stream"
    )


@account_info_router.get("/connect")
async def connect_ib():
    if ib.isConnected():
        return ApiResponse.success("IB already connected")
    try:
        await ib.connectAsync(
            get_settings().TWS_HOST, get_settings().TWS_PORT, clientId=1
        )
        return ApiResponse.success("IB connected")
    except Exception as e:
        return ApiResponse.error(f"IB connection failed: {e}")


@account_info_router.get("/disconnect")
async def disconnect_ib():
    if not ib.isConnected():
        return ApiResponse.error("IB not connected")
    ib.disconnect()
    return ApiResponse.success("IB disconnected")


@account_info_router.get("/pnl")
async def get_account_pnl():
    pnl = ib.pnl()
    return ApiResponse.success(pnl)


@account_info_router.get("/positions")
async def get_account_positions():
    positions = ib.positions()
    return ApiResponse.success(positions)


@account_info_router.get("/portfolio")
async def get_account_portfolio():
    portfolio = ib.portfolio()
    return ApiResponse.success(portfolio)


@account_info_router.get("/trades")
async def get_account_trades():
    trades = ib.trades()
    return ApiResponse.success(trades)
