import asyncio
import json
from datetime import datetime
from typing import Dict, Set, Optional, List
from fastapi import WebSocket, WebSocketDisconnect
from ib_async import Trade
from core import ib
from utils.logger import logger


class WebSocketManager:
    """WebSocket连接管理器"""

    def __init__(self):
        # 存储活跃的WebSocket连接
        self.active_connections: Dict[str, WebSocket] = {}
        # 订阅的消息类型
        self.subscriptions: Dict[str, Set[str]] = {}
        # 订单监听任务
        self._order_monitoring_task: Optional[asyncio.Task] = None
        # 市场数据监听任务
        self._market_data_task: Optional[asyncio.Task] = None
        # 上一次的订单状态
        self._last_order_states: Dict[int, str] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        """建立WebSocket连接"""
        try:
            await websocket.accept()
            self.active_connections[client_id] = websocket
            self.subscriptions[client_id] = set()

            logger.info(f"客户端 {client_id} 已连接WebSocket")

            # 发送连接成功消息
            await self.send_to_client(
                client_id,
                {
                    "type": "connection",
                    "status": "connected",
                    "message": "WebSocket连接成功",
                    "timestamp": datetime.now().isoformat(),
                    "client_id": client_id,
                },
            )

            # 启动订单监听（如果还没有启动）
            if (
                self._order_monitoring_task is None
                or self._order_monitoring_task.done()
            ):
                self._order_monitoring_task = asyncio.create_task(
                    self._monitor_orders()
                )

        except Exception as e:
            logger.error(f"WebSocket连接失败: {str(e)}")
            raise

    async def disconnect(self, client_id: str):
        """断开WebSocket连接"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.subscriptions:
            del self.subscriptions[client_id]

        logger.info(f"客户端 {client_id} 已断开WebSocket连接")

        # 如果没有活跃连接，停止监听任务
        if not self.active_connections:
            if self._order_monitoring_task and not self._order_monitoring_task.done():
                self._order_monitoring_task.cancel()
            if self._market_data_task and not self._market_data_task.done():
                self._market_data_task.cancel()

    async def send_to_client(self, client_id: str, message: dict):
        """向特定客户端发送消息"""
        if client_id in self.active_connections:
            try:
                websocket = self.active_connections[client_id]
                await websocket.send_text(json.dumps(message, ensure_ascii=False))
            except WebSocketDisconnect:
                await self.disconnect(client_id)
            except Exception as e:
                logger.error(f"向客户端 {client_id} 发送消息失败: {str(e)}")
                await self.disconnect(client_id)

    async def broadcast(self, message: dict, message_type: str = None):
        """广播消息给所有订阅的客户端"""
        if not self.active_connections:
            return

        # 如果指定了消息类型，只发送给订阅了该类型的客户端
        target_clients = []
        if message_type:
            for client_id, subscriptions in self.subscriptions.items():
                if message_type in subscriptions:
                    target_clients.append(client_id)
        else:
            target_clients = list(self.active_connections.keys())

        # 并发发送消息
        tasks = []
        for client_id in target_clients:
            task = self.send_to_client(client_id, message)
            tasks.append(task)

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def subscribe(self, client_id: str, message_types: List[str]):
        """客户端订阅消息类型"""
        if client_id not in self.subscriptions:
            self.subscriptions[client_id] = set()

        for msg_type in message_types:
            self.subscriptions[client_id].add(msg_type)

        logger.info(f"客户端 {client_id} 订阅了消息类型: {message_types}")

        # 发送订阅确认
        await self.send_to_client(
            client_id,
            {
                "type": "subscription",
                "status": "success",
                "subscribed_types": list(self.subscriptions[client_id]),
                "timestamp": datetime.now().isoformat(),
            },
        )

    async def unsubscribe(self, client_id: str, message_types: List[str]):
        """客户端取消订阅消息类型"""
        if client_id in self.subscriptions:
            for msg_type in message_types:
                self.subscriptions[client_id].discard(msg_type)

        logger.info(f"客户端 {client_id} 取消订阅了消息类型: {message_types}")

        # 发送取消订阅确认
        await self.send_to_client(
            client_id,
            {
                "type": "unsubscription",
                "status": "success",
                "remaining_types": list(self.subscriptions.get(client_id, [])),
                "timestamp": datetime.now().isoformat(),
            },
        )

    async def _monitor_orders(self):
        """监听订单状态变化"""
        logger.info("开始监听订单状态变化")

        while self.active_connections:
            try:
                if ib.isConnected():
                    # 获取当前所有订单
                    trades = ib.trades()

                    for trade in trades:
                        perm_id = trade.order.permId
                        current_status = trade.orderStatus.status

                        # 检查订单状态是否有变化
                        if (
                            perm_id not in self._last_order_states
                            or self._last_order_states[perm_id] != current_status
                        ):
                            # 更新订单状态记录
                            self._last_order_states[perm_id] = current_status

                            # 准备订单状态消息
                            order_message = {
                                "type": "order_update",
                                "data": {
                                    "perm_id": perm_id,
                                    "order_id": trade.order.orderId,
                                    "symbol": trade.contract.symbol,
                                    "action": trade.order.action,
                                    "quantity": trade.order.totalQuantity,
                                    "order_type": trade.order.orderType,
                                    "status": current_status,
                                    "filled": trade.filled(),
                                    "remaining": trade.remaining(),
                                    "avg_fill_price": trade.orderStatus.avgFillPrice,
                                    "price": (
                                        getattr(trade.order, "lmtPrice", None)
                                        or getattr(trade.order, "stopPrice", None)
                                    ),
                                    "why_held": trade.orderStatus.whyHeld,
                                },
                                "timestamp": datetime.now().isoformat(),
                            }

                            # 广播订单状态更新
                            await self.broadcast(order_message, "order_update")

                            logger.info(f"订单 {perm_id} 状态更新: {current_status}")

                # 等待一段时间再检查
                await asyncio.sleep(1)

            except Exception as e:
                logger.error(f"订单监听过程中出现错误: {str(e)}")
                await asyncio.sleep(5)  # 错误时等待更长时间

        logger.info("订单监听任务结束")

    async def send_order_notification(self, trade: Trade, action: str = "created"):
        """发送订单通知"""
        message = {
            "type": "order_notification",
            "action": action,
            "data": {
                "order_id": trade.order.orderId,
                "symbol": trade.contract.symbol,
                "action": trade.order.action,
                "quantity": trade.order.totalQuantity,
                "order_type": trade.order.orderType,
                "status": trade.orderStatus.status,
                "price": (
                    getattr(trade.order, "lmtPrice", None)
                    or getattr(trade.order, "stopPrice", None)
                ),
            },
            "message": f"订单{action}成功",
            "timestamp": datetime.now().isoformat(),
        }

        await self.broadcast(message, "order_notification")

    async def send_account_update(self, account_data: dict):
        """发送账户信息更新"""
        message = {
            "type": "account_update",
            "data": account_data,
            "timestamp": datetime.now().isoformat(),
        }

        await self.broadcast(message, "account_update")

    async def send_market_data(self, symbol: str, market_data: dict):
        """发送市场数据"""
        message = {
            "type": "market_data",
            "symbol": symbol,
            "data": market_data,
            "timestamp": datetime.now().isoformat(),
        }

        await self.broadcast(message, "market_data")

    async def send_error_notification(self, error_message: str, error_code: str = None):
        """发送错误通知"""
        message = {
            "type": "error",
            "message": error_message,
            "error_code": error_code,
            "timestamp": datetime.now().isoformat(),
        }

        await self.broadcast(message, "error")

    async def handle_client_message(self, client_id: str, message: dict):
        """处理客户端发送的消息"""
        try:
            msg_type = message.get("type")

            if msg_type == "subscribe":
                message_types = message.get("message_types", [])
                await self.subscribe(client_id, message_types)

            elif msg_type == "unsubscribe":
                message_types = message.get("message_types", [])
                await self.unsubscribe(client_id, message_types)

            elif msg_type == "ping":
                # 心跳检测
                await self.send_to_client(
                    client_id, {"type": "pong", "timestamp": datetime.now().isoformat()}
                )

            elif msg_type == "get_orders":
                # 获取当前订单状态
                if ib.isConnected():
                    trades = ib.trades()
                    orders_data = []
                    for trade in trades:
                        orders_data.append(
                            {
                                "order_id": trade.order.orderId,
                                "symbol": trade.contract.symbol,
                                "action": trade.order.action,
                                "quantity": trade.order.totalQuantity,
                                "order_type": trade.order.orderType,
                                "status": trade.orderStatus.status,
                                "filled": trade.filled(),
                                "remaining": trade.remaining(),
                                "avg_fill_price": trade.orderStatus.avgFillPrice,
                                "price": (
                                    getattr(trade.order, "lmtPrice", None)
                                    or getattr(trade.order, "stopPrice", None)
                                ),
                            }
                        )

                    await self.send_to_client(
                        client_id,
                        {
                            "type": "orders_response",
                            "data": orders_data,
                            "timestamp": datetime.now().isoformat(),
                        },
                    )
                else:
                    await self.send_to_client(
                        client_id,
                        {
                            "type": "error",
                            "message": "IB TWS未连接",
                            "timestamp": datetime.now().isoformat(),
                        },
                    )

            else:
                await self.send_to_client(
                    client_id,
                    {
                        "type": "error",
                        "message": f"未知的消息类型: {msg_type}",
                        "timestamp": datetime.now().isoformat(),
                    },
                )

        except Exception as e:
            logger.error(f"处理客户端消息时出错: {str(e)}")
            await self.send_to_client(
                client_id,
                {
                    "type": "error",
                    "message": f"处理消息时出错: {str(e)}",
                    "timestamp": datetime.now().isoformat(),
                },
            )

    def get_connection_count(self) -> int:
        """获取当前连接数"""
        return len(self.active_connections)

    def get_connected_clients(self) -> List[str]:
        """获取已连接的客户端ID列表"""
        return list(self.active_connections.keys())


# 创建全局WebSocket管理器实例
websocket_manager = WebSocketManager()
