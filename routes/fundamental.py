from fastapi import APIRouter, Query
from core.fundamental_operate import (
    get_company_profile,
    get_financial_statements,
    get_analyst_estimates,
    get_ownership_data,
)
from utils.data_convert import ApiResponse

fundamental_router = APIRouter(tags=["fundamental"])


@fundamental_router.get("/profile/{symbol}")
async def get_profile(
    symbol: str,
    exchange: str = Query(default="SMART", description="交易所代码"),
):
    """获取公司概况"""
    try:
        _, profile = await get_company_profile(symbol, exchange)
        return ApiResponse.success(profile)
    except Exception as e:
        return ApiResponse.error(f"获取公司概况失败: {str(e)}")


@fundamental_router.get("/financials/{symbol}")
async def get_financials(
    symbol: str,
    exchange: str = Query(default="SMART", description="交易所代码"),
):
    """获取财务报表"""
    try:
        _, statements = await get_financial_statements(symbol, exchange)
        return ApiResponse.success(statements)
    except Exception as e:
        return ApiResponse.error(f"获取财务报表失败: {str(e)}")


@fundamental_router.get("/estimates/{symbol}")
async def get_estimates(
    symbol: str,
    exchange: str = Query(default="SMART", description="交易所代码"),
):
    """获取分析师预测"""
    try:
        _, estimates = await get_analyst_estimates(symbol, exchange)
        return ApiResponse.success(estimates)
    except Exception as e:
        return ApiResponse.error(f"获取分析师预测失败: {str(e)}")


@fundamental_router.get("/ownership/{symbol}")
async def get_ownership(
    symbol: str,
    exchange: str = Query(default="SMART", description="交易所代码"),
):
    """获取所有权数据"""
    try:
        _, ownership = await get_ownership_data(symbol, exchange)
        return ApiResponse.success(ownership)
    except Exception as e:
        return ApiResponse.error(f"获取所有权数据失败: {str(e)}")
