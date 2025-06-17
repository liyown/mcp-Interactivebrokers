from fastapi import FastAPI, Request, Response
from mcp_server import mcp_app
import uvicorn
from routes.account_info import account_info_router
from routes.market_data import market_data_router
from routes.fundamental import fundamental_router
from routes.trading import trading_router
from routes.websocket import websocket_router
from core import ib
from utils.data_convert import ApiResponse
from core.config import get_settings
from utils.logger import logger

settings = get_settings()

# 创建 FastAPI 应用
fast_app = FastAPI(
    title="Interactive Brokers API",
    description="Interactive Brokers API wrapper with FastAPI and FastMCP",
    version="0.1.0",
    lifespan=mcp_app.lifespan,
    root_path=settings.API_ROOT_PATH,
)

# 挂载 MCP 服务器和路由
fast_app.mount("/mcp-server", mcp_app)
fast_app.include_router(account_info_router, prefix="/account_info")
fast_app.include_router(market_data_router, prefix="/market_data")
fast_app.include_router(fundamental_router, prefix="/fundamental")
fast_app.include_router(trading_router, prefix="/trading")
fast_app.include_router(websocket_router, prefix="/websocket")


@fast_app.middleware("http")
async def ib_status_middleware(request: Request, call_next):
    if request.url.path == f"{settings.API_ROOT_PATH}/account_info/connect":
        return await call_next(request)

    if ib.isConnected():
        return await call_next(request)

    else:
        logger.warning("尝试访问 API 时 IB TWS 未连接")
        return Response(
            content=ApiResponse.error("IB TWS is not connected").to_json(),
        )


if __name__ == "__main__":
    uvicorn.run(
        "main:fast_app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        log_level=settings.LOG_LEVEL.lower(),
    )
