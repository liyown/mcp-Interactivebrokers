from core import ib


# def get_fundamental_data(symbol: str):
#     company_financials = CompanyFinancials(symbol=symbol, ib=ib)
#     print(company_financials.company_information)


def get_portfolio():
    portfolio = ib.portfolio()

    formatted_portfolio = []
    for position in portfolio:
        formatted_portfolio.append(
            f"""<position>
                <symbol>
                    <value>{position.contract.symbol}</value>
                    <description>Stock symbol</description>
                </symbol>
                <exchange>
                    <value>{position.contract.exchange}</value>
                    <description>Trading exchange</description>
                </exchange>
                <currency>
                    <value>{position.contract.currency}</value>
                    <description>Currency denomination</description>
                </currency>
                <quantity>
                    <value>{position.position}</value>
                    <description>Position size</description>
                </quantity>
                <marketPrice>
                    <value>{position.marketPrice}</value>
                    <description>Current market price</description>
                </marketPrice>
                <marketValue>
                    <value>{position.marketValue}</value>
                    <description>Total market value</description>
                </marketValue>
                <averageCost>
                    <value>{position.averageCost}</value>
                    <description>Average cost basis</description>
                </averageCost>
                <unrealizedPNL>
                    <value>{position.unrealizedPNL}</value>
                    <description>Unrealized profit/loss</description>
                </unrealizedPNL>
                <realizedPNL>
                    <value>{position.realizedPNL}</value>
                    <description>Realized profit/loss</description>
                </realizedPNL>
            </position>"""
        )
    return formatted_portfolio


def get_pnl():
    pnl = ib.pnl()
    return f"""<pnl>
        <value>{pnl}</value>
        <description>Current profit and loss information</description>
    </pnl>"""


def get_account_summary():
    account_summary = ib.accountValues()

    # Define valuable fields with descriptions
    valuable_fields = {
        "NetLiquidation": "Total account value including cash, securities and unrealized P&L",
        "AvailableFunds": "Cash available for purchasing securities",
        "BuyingPower": "Total amount available for purchasing securities including margin",
        "EquityWithLoanValue": "Total stock value including loans",
        "ExcessLiquidity": "Available funds exceeding margin requirements",
        "InitMarginReq": "Initial margin requirement for opening positions",
        "MaintMarginReq": "Maintenance margin requirement for existing positions",
        "GrossPositionValue": "Total market value of all positions",
        "TotalCashValue": "Total cash in the account",
        "UnrealizedPnL": "Unrealized profit/loss on current positions",
        "RealizedPnL": "Realized profit/loss from closed trades",
        "StockMarketValue": "Total market value of stock positions",
        "CashBalance": "Available cash balance",
    }

    # Process account summary
    result = "<accountSummary>"
    for value in account_summary:
        if value.tag in valuable_fields:
            result += f"""
                <{value.tag}>
                    <value>{value.value}</value>
                    <description>{valuable_fields[value.tag]}</description>
                </{value.tag}>"""
    result += "</accountSummary>"

    return result
