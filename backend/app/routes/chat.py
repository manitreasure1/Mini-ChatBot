from fastapi import WebSocket, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from config.socket_ import ConnectionManager


router = APIRouter(tags=["Chat"])
manager = ConnectionManager()

@router.websocket("/ws/send-message")
def send_message(socket: WebSocket): ...


@router.get("/chat-history")
def chat_history():
    try:

        return JSONResponse("", status_code=status.HTTP_200_OK)
    except HTTPException as e:
        raise e
