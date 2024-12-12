from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Додавання CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Зберігаємо підключення для кожної зустрічі
meetings_connections = {}

@app.websocket("/ws/{meeting_id}")
async def websocket_endpoint(websocket: WebSocket, meeting_id: str):
    await websocket.accept()
    if meeting_id not in meetings_connections:
        meetings_connections[meeting_id] = []
    meetings_connections[meeting_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # Розсилаємо повідомлення всім у зустрічі
            for connection in meetings_connections[meeting_id]:
                if connection != websocket:
                    print(data)
                    await connection.send_text(data)
    except WebSocketDisconnect:
        meetings_connections[meeting_id].remove(websocket)
