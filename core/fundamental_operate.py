from ib_async import Stock
from core import ib
from core.constant import FundamentalDataType


def get_company_profile(symbol: str, exchange: str = "SMART"):
    """获取公司概况"""
    contract = Stock(symbol, exchange, "USD")
    ib.qualifyContracts(contract)

    profile = ib.reqFundamentalData(
        contract, reportType=FundamentalDataType.REPORT_SNAPSHOT.value
    )

    return f"""<companyProfile>
        <data>
            <value>{profile}</value>
            <description>Company profile data</description>
        </data>
    </companyProfile>"""


def get_financial_statements(
    symbol: str,
    exchange: str = "SMART",
):
    """获取财务报表"""
    contract = Stock(symbol, exchange, "USD")
    ib.qualifyContracts(contract)

    statements = ib.reqFundamentalData(
        contract, reportType=FundamentalDataType.REPORTS_FIN_STATEMENTS.value
    )

    return f"""<financialStatements>
        <data>
            <value>{statements}</value>
            <description>Financial statements data</description>
        </data>
    </financialStatements>"""


def get_analyst_estimates(
    symbol: str,
    exchange: str = "SMART",
):
    """获取分析师预测"""
    contract = Stock(symbol, exchange, "USD")
    ib.qualifyContracts(contract)

    estimates = ib.reqFundamentalData(
        contract, reportType=FundamentalDataType.RESC.value
    )

    return f"""<analystEstimates>
        <data>
            <value>{estimates}</value>
            <description>Analyst estimates data</description>
        </data>
    </analystEstimates>"""


def get_ownership_data(
    symbol: str,
    exchange: str = "SMART",
):
    """获取所有权数据"""
    contract = Stock(symbol, exchange, "USD")
    ib.qualifyContracts(contract)

    ownership = ib.reqFundamentalData(
        contract, reportType=FundamentalDataType.REPORTS_OWNERSHIP.value
    )

    return f"""<ownershipData>
        <data>
            <value>{ownership}</value>
            <description>Ownership data</description>
        </data>
    </ownershipData>"""
