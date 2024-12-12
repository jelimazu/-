import threading
import websocket
import json
from tkinter import simpledialog
from client.views.chat_view import ChatView


class ChatController:
    def __init__(self, meeting_id):
        self.meeting_id = meeting_id
        # Запит нікнейму у користувача
        self.nickname = simpledialog.askstring("Nickname", "Enter your nickname:")
        if not self.nickname:
            self.nickname = "Anonymous"

        self.view = ChatView(self)

        # Адреса WebSocket-сервера
        self.ws_url = f"ws://127.0.0.1:8000/ws/{self.meeting_id}"

        # Створюємо WebSocket підключення в окремому потоці
        self.ws = None
        self.running = True
        self.connect_websocket()

    def connect_websocket(self):
        def run_ws():
            self.ws = websocket.WebSocketApp(
                self.ws_url,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )

            # Відкриваємо з'єднання
            self.ws.on_open = self.on_open
            self.ws.run_forever()

        threading.Thread(target=run_ws, daemon=True).start()

    def on_open(self, ws):
        self.view.add_message("System", f"Connected to meeting {self.meeting_id} chat as {self.nickname}.")

    def on_message(self, ws, message):
        # Повідомлення приходить у текстовому форматі. Маємо очікувати JSON.
        try:
            data = json.loads(message)
            sender = data.get("sender", "Unknown")
            msg_text = data.get("message", "")
            self.view.add_message(sender, msg_text)
        except json.JSONDecodeError:
            # Якщо повідомлення не JSON, просто покажемо як є (на всяк випадок)
            self.view.add_message("Unknown", message)

    def on_error(self, ws, error):
        self.view.add_message("System", f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        self.view.add_message("System", f"WebSocket closed: {close_msg}")

    def send_message(self, message):
        if self.ws and self.running:
            # Надсилаємо повідомлення у форматі JSON з sender та message
            data = {"sender": self.nickname, "message": message}
            self.ws.send(json.dumps(data))
            # Локально також додаємо у вікно чату від себе
            self.view.add_message(self.nickname, message)
        else:
            self.view.add_message("System", "Not connected.")

    def stop(self):
        self.running = False
        if self.ws:
            self.ws.close()
