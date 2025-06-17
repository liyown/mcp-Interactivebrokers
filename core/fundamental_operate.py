from ib_async import Stock
from core import ib
from core.constant import FundamentalDataType


async def get_company_profile(symbol: str, exchange: str = "SMART"):
    """获取公司概况"""
    contract = Stock(symbol, exchange, "USD")
    await ib.qualifyContractsAsync(contract)

    profile = await ib.reqFundamentalDataAsync(
        contract, reportType=FundamentalDataType.REPORT_SNAPSHOT.value
    )

    return (
        f"""<companyProfile>
        <data>
            <value>{profile}</value>
            <description>Company profile data</description>
        </data>
    </companyProfile>""",
        profile,
    )


async def get_financial_statements(
    symbol: str,
    exchange: str = "SMART",
):
    """获取财务报表"""
    contract = Stock(symbol, exchange, "USD")
    await ib.qualifyContractsAsync(contract)

    statements = await ib.reqFundamentalDataAsync(
        contract, reportType=FundamentalDataType.REPORTS_FIN_STATEMENTS.value
    )

    return (
        f"""<financialStatements>
        <data>
            <value>{statements}</value>
            <description>Financial statements data</description>
        </data>
    </financialStatements>""",
        statements,
    )


async def get_analyst_estimates(
    symbol: str,
    exchange: str = "SMART",
):
    """获取分析师预测"""
    contract = Stock(symbol, exchange, "USD")
    await ib.qualifyContractsAsync(contract)

    estimates = await ib.reqFundamentalDataAsync(
        contract, reportType=FundamentalDataType.RESC.value
    )

    return (
        f"""<analystEstimates>
        <data>
            <value>{estimates}</value>
            <description>Analyst estimates data</description>
        </data>
    </analystEstimates>""",
        estimates,
    )


async def get_ownership_data(
    symbol: str,
    exchange: str = "SMART",
):
    """获取所有权数据"""
    contract = Stock(symbol, exchange, "USD")
    await ib.qualifyContractsAsync(contract)

    ownership = await ib.reqFundamentalDataAsync(
        contract, reportType=FundamentalDataType.REPORTS_OWNERSHIP.value
    )

    return (
        f"""<ownershipData>
        <data>
            <value>{ownership}</value>
            <description>Ownership data</description>
        </data>
    </ownershipData>""",
        ownership,
    )
