from ib_async import Stock
from core import ib
from typing import Optional
from datetime import datetime


def get_stock_quote(symbol: str, exchange: str = "SMART", currency: str = "USD"):
    """获取股票实时报价"""
    contract = Stock(symbol, exchange, currency)
    ib.qualifyContracts(contract)

    # 请求市场数据
    ticker = ib.reqMktData(contract)
    try:
        ib.sleep(2)  # 等待数据返回
        return f"""<quote>
            <symbol>
                <value>{contract.symbol}</value>
                <description>Stock symbol</description>
            </symbol>
            <lastPrice>
                <value>{ticker.last}</value>
                <description>Last trade price</description>
            </lastPrice>
            <bid>
                <value>{ticker.bid}</value>
                <description>Bid price</description>
            </bid>
            <ask>
                <value>{ticker.ask}</value>
                <description>Ask price</description>
            </ask>
            <volume>
                <value>{ticker.volume}</value>
                <description>Trading volume</description>
            </volume>
            <high>
                <value>{ticker.high}</value>
                <description>Day high</description>
            </high>
            <low>
                <value>{ticker.low}</value>
                <description>Day low</description>
            </low>
        </quote>"""
    finally:
        ib.cancelMktData(contract)


def get_historical_data(
    symbol: str,
    duration: str = "1 D",
    bar_size: str = "1 min",
    exchange: str = "SMART",
    currency: str = "USD",
    end_datetime: Optional[datetime] = None,
):
    """获取历史数据

    Args:
        symbol: 股票代码
        duration: 数据时长，如 "1 D", "1 W", "1 M", "1 Y"
        bar_size: K线周期，如 "1 min", "5 mins", "1 hour", "1 day"
        exchange: 交易所
        currency: 货币
        end_datetime: 结束时间，默认为当前时间
    """
    contract = Stock(symbol, exchange, currency)
    ib.qualifyContracts(contract)

    if end_datetime is None:
        end_datetime = datetime.now()

    bars = ib.reqHistoricalData(
        contract,
        endDateTime=end_datetime,
        durationStr=duration,
        barSizeSetting=bar_size,
        whatToShow="TRADES",
        useRTH=True,
    )

    formatted_bars = []
    for bar in bars:
        formatted_bars.append(f"""<bar>
            <time>
                <value>{bar.date}</value>
                <description>Bar time</description>
            </time>
            <open>
                <value>{bar.open}</value>
                <description>Open price</description>
            </open>
            <high>
                <value>{bar.high}</value>
                <description>High price</description>
            </high>
            <low>
                <value>{bar.low}</value>
                <description>Low price</description>
            </low>
            <close>
                <value>{bar.close}</value>
                <description>Close price</description>
            </close>
            <volume>
                <value>{bar.volume}</value>
                <description>Trading volume</description>
            </volume>
        </bar>""")

    return formatted_bars


def get_option_chain(
    symbol: str,
    exchange: str = "SMART",
    currency: str = "USD",
):
    """获取期权链数据"""
    stock = Stock(symbol, exchange, currency)
    ib.qualifyContracts(stock)

    chains = ib.reqSecDefOptParams(stock.symbol, "", stock.secType, stock.conId)

    formatted_chains = []
    for chain in chains:
        formatted_chains.append(f"""<optionChain>
            <exchange>
                <value>{chain.exchange}</value>
                <description>Option exchange</description>
            </exchange>
            <strikes>
                <value>{",".join(map(str, chain.strikes[:5]))}</value>
                <description>Available strike prices (first 5)</description>
            </strikes>
            <expirations>
                <value>{",".join(chain.expirations[:5])}</value>
                <description>Available expiration dates (first 5)</description>
            </expirations>
        </optionChain>""")

    return formatted_chains
