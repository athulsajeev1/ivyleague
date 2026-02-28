from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websockets import manager
import json

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            # Broadcast message to all connected users for community chat
            await manager.broadcast(json.dumps({
                "user_id": user_id,
                "message": message_data["message"],
                "type": "chat"
            }))
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
        await manager.broadcast(f"User #{user_id} left the chat")
