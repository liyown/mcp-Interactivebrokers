# Interactive Brokers API 服务

这是一个基于 FastAPI 和 FastMCP 的 Interactive Brokers API 包装器，提供了简单易用的 REST API 接口来与 Interactive Brokers 进行交互。

## 功能特点

- 账户管理
  - 账户连接状态监控
  - 账户摘要信息
  - 投资组合查询
  - 盈亏查询
  - 持仓查询

- 市场数据
  - 实时报价
  - 历史K线数据
  - 期权链数据

- 基本面数据
  - 公司概况
  - 财务报表
  - 分析师预测
  - 所有权数据

- 交易功能
  - 多种订单类型支持
    - 限价单
    - 市价单
    - 止损单
    - 止损限价单
  - 订单管理
    - 修改订单
    - 取消订单
    - 订单状态查询

## 系统要求

- Python 3.13+ / uv
- Interactive Brokers Trader Workstation (TWS) 或 IB Gateway

## 安装

1. 克隆仓库并进入项目目录

2. 安装依赖：
```bash
uv sync
```

## 配置

配置文件位置：
```shell
core/config.py
```

主要配置项：
- TWS 连接设置（主机、端口、客户端ID）
- API 服务器设置（主机、端口、根路径）
- 日志设置（级别、文件路径）

## 启动服务

1. 确保 TWS 或 IB Gateway 已经运行并启用 API 连接

2. 启动服务器：
```bash
uv run main.py
```

## API 端点

### MCP

- `GET /ib_api/mcp-server/sse` - 连接到 TWS

### 账户信息

- `GET /ib_api/account_info/connect` - 连接到 TWS
- `GET /ib_api/account_info/account_status` - 获取连接状态
- `GET /ib_api/account_info/disconnect` - 断开连接
- `GET /ib_api/account_info/summary` - 获取账户摘要
- `GET /ib_api/account_info/portfolio` - 获取投资组合
- `GET /ib_api/account_info/positions` - 获取持仓信息
- `GET /ib_api/account_info/pnl` - 获取盈亏信息

### 市场数据

- `GET /ib_api/market_data/quote/{symbol}` - 获取实时报价
  - 参数：
    - `exchange` - 交易所代码（默认：SMART）
    - `currency` - 货币代码（默认：USD）

- `GET /ib_api/market_data/history/{symbol}` - 获取历史数据
  - 参数：
    - `duration` - 数据时长（如：1 D, 1 W, 1 M）
    - `bar_size` - K线周期（如：1 min, 5 mins, 1 hour）
    - `exchange` - 交易所代码
    - `currency` - 货币代码

- `GET /ib_api/market_data/options/{symbol}` - 获取期权链数据
  - 参数：
    - `exchange` - 交易所代码
    - `currency` - 货币代码

### 基本面数据

- `GET /ib_api/fundamental/profile/{symbol}` - 获取公司概况
- `GET /ib_api/fundamental/financials/{symbol}` - 获取财务报表
- `GET /ib_api/fundamental/estimates/{symbol}` - 获取分析师预测
- `GET /ib_api/fundamental/ownership/{symbol}` - 获取所有权数据

### 交易功能

- `POST /ib_api/trading/order/limit` - 创建限价单
  ```json
  {
    "symbol": "AAPL",
    "quantity": 100,
    "price": 150.0,
    "action": "BUY",
    "exchange": "SMART",
    "currency": "USD",
    "tif": "DAY"
  }
  ```

- `POST /ib_api/trading/order/market` - 创建市价单
  ```json
  {
    "symbol": "AAPL",
    "quantity": 100,
    "action": "BUY",
    "exchange": "SMART",
    "currency": "USD"
  }
  ```

- `POST /ib_api/trading/order/stop` - 创建止损单
  ```json
  {
    "symbol": "AAPL",
    "quantity": 100,
    "stop_price": 145.0,
    "action": "SELL",
    "exchange": "SMART",
    "currency": "USD"
  }
  ```

- `POST /ib_api/trading/order/stop-limit` - 创建止损限价单
  ```json
  {
    "symbol": "AAPL",
    "quantity": 100,
    "stop_price": 145.0,
    "limit_price": 144.0,
    "action": "SELL",
    "exchange": "SMART",
    "currency": "USD"
  }
  ```

- `PUT /ib_api/trading/order/{order_id}` - 修改订单
  ```json
  {
    "quantity": 200,
    "price": 155.0
  }
  ```

- `DELETE /ib_api/trading/order/{order_id}` - 取消订单
- `GET /ib_api/trading/order/{order_id}` - 获取订单状态
- `GET /ib_api/trading/orders` - 获取所有订单


## 注意事项

1. 在使用 API 之前，请确保：
   - TWS 或 IB Gateway 已启动
   - API 连接已启用
   - 端口设置正确

## 许可证

MIT

## 贡献

欢迎提交 Issue 和 Pull Request！