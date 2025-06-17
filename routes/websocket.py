import json
import uuid
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from core.websocket import websocket_manager
from utils.logger import logger

websocket_router = APIRouter(tags=["websocket"])


@websocket_router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str = Query(None, description="客户端ID，如果不提供会自动生成"),
):
    """
    WebSocket连接端点

    支持的消息类型：
    - subscribe: 订阅消息类型
    - unsubscribe: 取消订阅消息类型
    - ping: 心跳检测
    - get_orders: 获取当前订单状态

    推送的消息类型：
    - order_update: 订单状态更新
    - order_notification: 订单通知
    - account_update: 账户信息更新
    - market_data: 市场数据
    - error: 错误通知
    """

    # 如果没有提供客户端ID，自动生成一个
    if not client_id:
        client_id = str(uuid.uuid4())

    try:
        # 建立WebSocket连接
        await websocket_manager.connect(websocket, client_id)

        # 监听客户端消息
        while True:
            try:
                # 接收客户端消息
                data = await websocket.receive_text()
                message = json.loads(data)

                # 处理客户端消息
                await websocket_manager.handle_client_message(client_id, message)

            except WebSocketDisconnect:
                logger.info(f"客户端 {client_id} 主动断开连接")
                break
            except json.JSONDecodeError:
                await websocket_manager.send_to_client(
                    client_id,
                    {
                        "type": "error",
                        "message": "无效的JSON格式",
                        "timestamp": datetime.now().isoformat(),
                    },
                )
            except Exception as e:
                logger.error(f"处理WebSocket消息时出错: {str(e)}")
                await websocket_manager.send_to_client(
                    client_id,
                    {
                        "type": "error",
                        "message": f"处理消息时出错: {str(e)}",
                        "timestamp": datetime.now().isoformat(),
                    },
                )

    except Exception as e:
        logger.error(f"WebSocket连接出错: {str(e)}")

    finally:
        # 断开连接时清理
        await websocket_manager.disconnect(client_id)


@websocket_router.get("/ws/status")
async def get_websocket_status():
    """获取WebSocket连接状态"""
    return {
        "active_connections": websocket_manager.get_connection_count(),
        "connected_clients": websocket_manager.get_connected_clients(),
        "total_subscriptions": sum(
            len(subs) for subs in websocket_manager.subscriptions.values()
        ),
    }


@websocket_router.post("/ws/broadcast")
async def broadcast_message(message: dict, message_type: str = None):
    """
    手动广播消息（用于测试或管理）
    """
    try:
        await websocket_manager.broadcast(message, message_type)
        return {
            "status": "success",
            "message": "消息已广播",
            "target_clients": websocket_manager.get_connection_count(),
        }
    except Exception as e:
        return {"status": "error", "message": f"广播失败: {str(e)}"}
