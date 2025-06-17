# Interactive Brokers WebSocket 实时通知系统使用说明

## 概述

本系统通过WebSocket技术实现了Interactive Brokers交易平台的实时通知功能，可以实时推送订单状态、MCP操作、账户更新等信息到客户端。

## 功能特点

- 实时订单状态更新
- MCP订单操作通知
- 账户信息更新
- 市场数据推送
- 错误通知
- 支持多客户端连接
- 消息类型订阅机制
- 心跳检测

## 连接方式

WebSocket连接地址：`ws://localhost:8000/websocket/ws`

可选参数：
- `client_id`: 客户端ID，如果不提供会自动生成

示例：
```
ws://localhost:8000/websocket/ws?client_id=my_client_001
```

## 消息类型

### 客户端可订阅的消息类型

1. `order_update`: 订单状态更新
2. `order_notification`: 订单通知（创建、修改、取消）
3. `mcp_order`: MCP订单操作
4. `account_update`: 账户信息更新
5. `market_data`: 市场数据
6. `error`: 错误通知

### 客户端可发送的消息类型

1. `subscribe`: 订阅消息类型
   ```json
   {
     "type": "subscribe",
     "message_types": ["order_update", "order_notification", "mcp_order"]
   }
   ```

2. `unsubscribe`: 取消订阅消息类型
   ```json
   {
     "type": "unsubscribe",
     "message_types": ["order_update"]
   }
   ```

3. `ping`: 心跳检测
   ```json
   {
     "type": "ping"
   }
   ```

4. `get_orders`: 获取当前订单状态
   ```json
   {
     "type": "get_orders"
   }
   ```

## 消息格式

### 订单状态更新 (order_update)

```json
{
  "type": "order_update",
  "data": {
    "order_id": 12345,
    "symbol": "AAPL",
    "action": "BUY",
    "quantity": 100,
    "order_type": "LMT",
    "status": "Submitted",
    "filled": 0,
    "remaining": 100,
    "avg_fill_price": 0,
    "price": 150.25,
    "why_held": ""
  },
  "timestamp": "2023-03-15T10:30:45.123456"
}
```

### 订单通知 (order_notification)

```json
{
  "type": "order_notification",
  "action": "创建",
  "data": {
    "order_id": 12345,
    "symbol": "AAPL",
    "action": "BUY",
    "quantity": 100,
    "order_type": "LMT",
    "status": "Submitted",
    "price": 150.25
  },
  "message": "订单创建成功",
  "timestamp": "2023-03-15T10:30:45.123456"
}
```

### MCP订单操作 (mcp_order)

```json
{
  "type": "mcp_order",
  "action": "MCP创建限价单",
  "data": {
    "order_id": 12345,
    "symbol": "AAPL",
    "action": "BUY",
    "quantity": 100,
    "order_type": "LMT",
    "price": 150.25,
    "status": "Submitted"
  },
  "source": "MCP",
  "message": "MCP 创建限价单",
  "timestamp": "2023-03-15T10:30:45.123456"
}
```

### 错误通知 (error)

```json
{
  "type": "error",
  "message": "订单创建失败: 余额不足",
  "error_code": "INSUFFICIENT_FUNDS",
  "timestamp": "2023-03-15T10:30:45.123456"
}
```

## 使用示例

### Python客户端示例

```python
import asyncio
import websockets
import json

async def websocket_client():
    uri = "ws://localhost:8000/websocket/ws"
    async with websockets.connect(uri) as websocket:
        # 订阅消息类型
        await websocket.send(json.dumps({
            "type": "subscribe",
            "message_types": ["order_update", "order_notification", "mcp_order"]
        }))
        
        # 接收消息
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                print(f"收到消息: {data}")
            except websockets.exceptions.ConnectionClosed:
                print("连接已关闭")
                break
            except Exception as e:
                print(f"错误: {e}")
                break

asyncio.run(websocket_client())
```

### JavaScript客户端示例

```javascript
const ws = new WebSocket('ws://localhost:8000/websocket/ws');

ws.onopen = function() {
    console.log('连接已建立');
    
    // 订阅消息类型
    ws.send(JSON.stringify({
        type: 'subscribe',
        message_types: ['order_update', 'order_notification', 'mcp_order']
    }));
};

ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    console.log('收到消息:', message);
};

ws.onclose = function() {
    console.log('连接已关闭');
};

ws.onerror = function(error) {
    console.error('WebSocket错误:', error);
};
```

## 注意事项

1. 确保IB TWS已连接并正常运行
2. WebSocket连接可能会因为网络问题断开，建议实现自动重连机制
3. 对于重要操作，建议同时使用WebSocket通知和API响应
4. 客户端应该实现心跳检测，定期发送ping消息
5. 大量客户端连接时，注意服务器的资源消耗

## 故障排除

1. 连接失败
   - 检查服务器是否正常运行
   - 检查网络连接
   - 检查防火墙设置

2. 收不到消息
   - 确认已正确订阅消息类型
   - 检查订单操作是否成功
   - 查看服务器日志

3. 消息延迟
   - 检查网络状况
   - 检查服务器负载
   - 考虑优化消息处理逻辑

## 安全建议

1. 在生产环境中使用WSS（WebSocket Secure）
2. 实现客户端认证机制
3. 限制连接数量和消息频率
4. 对敏感信息进行加密
5. 定期清理断开的连接 