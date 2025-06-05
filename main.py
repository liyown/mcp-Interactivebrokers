from fastapi import FastAPI, Request, Response
from mcp_server import mcp_app
import uvicorn
from routes.account_info import account_info_router
from core import ib
from utils.data_convert import ApiResponse


fast_app = FastAPI(lifespan=mcp_app.lifespan, root_path="/ib_api")
fast_app.mount("/mcp-server", mcp_app)
fast_app.include_router(account_info_router, prefix="/account_info")


@fast_app.middleware("http")
async def ib_status_middleware(request: Request, call_next):
    if request.url.path == "/ib_api/account_info/connect":
        return await call_next(request)

    if ib.isConnected():
        return await call_next(request)
    else:
        return Response(
            content=ApiResponse.error("IB TWS is not connected").to_json(),
        )


if __name__ == "__main__":
    uvicorn.run(fast_app, host="0.0.0.0", port=1200)
