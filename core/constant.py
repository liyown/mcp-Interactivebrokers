from enum import Enum


class OrderType(Enum):
    LIMIT = "LMT"
    MARKET = "MKT"

class OrderAction(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderStatus(Enum):
    PENDING = "PENDING"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class FundamentalDataType(Enum):
    REPORTS_FIN_SUMMARY = "ReportsFinSummary"  # 财务摘要
    REPORTS_OWNERSHIP = "ReportsOwnership"  # 公司所有权
    REPORT_SNAPSHOT = "ReportSnapshot"  # 公司财务概览
    REPORTS_FIN_STATEMENTS = "ReportsFinStatements"  # 财务报表
    RESC = "RESC"  # 分析师预测
    CALENDAR_REPORT = "CalendarReport"  # 公司日历
    

