from fastapi import WebSocket
from starlette.websockets import WebSocketState

class ConnectionManager:
    def __init__(self, size: int):
        self._active_connections: dict[int, WebSocket] = {}
        self._connections: int = 0
        self._max_size: int = size

    def connections_amount(self) -> int:
        return self._connections
    
    def is_websocket_connected(self, ws:WebSocket) -> bool: 
        return ws.client_state == WebSocketState.CONNECTED


    async def connect(self, client_id: int, websocket: WebSocket):
        if client_id >= self._max_size or self._connections == self._max_size: return
        await websocket.accept()
        self._active_connections[client_id] = websocket
        self._connections += 1

    async def disconnect(self, client_id: int):
        ws: WebSocket = self._active_connections[client_id]
        if self.is_websocket_connected(ws):    
            await ws.close()
            self._connections -= 1

    async def send_to(self, client_id: int, message: str):

        ws: WebSocket = self._active_connections[client_id]
        if self.is_websocket_connected(ws): await ws.send_text(message)

    async def broadcast(self, message: str):
        for ws in self._active_connections:
            await self._active_connections[ws].send_text(message)

    async def shutdown(self):
        # hard coded because of strange bug
        for ws_index in self._active_connections:
            await self.disconnect(ws_index)
