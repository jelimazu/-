import tkinter as tk
from tkinter import scrolledtext

class ChatView(tk.Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Meeting Chat")

        # Зменшуємо розмір вікна для кращого вигляду у невеликому вікні
        self.geometry("700x500")

        # Основне текстове поле для відображення повідомлень
        self.chat_display = scrolledtext.ScrolledText(self, state='disabled', wrap='word', font=("Arial", 10))
        self.chat_display.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Фрейм для введення повідомлення і кнопки відправки
        self.entry_frame = tk.Frame(self)
        self.entry_frame.pack(fill=tk.X, padx=5, pady=5)

        self.message_entry = tk.Entry(self.entry_frame, font=("Arial", 10))
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.message_entry.bind("<Return>", self.send_message_event)

        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message, font=("Arial", 10))
        self.send_button.pack(side=tk.LEFT, padx=5)

        # При закритті вікна чату відключаємо WebSocket
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_message(self, sender, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def send_message(self):
        msg = self.message_entry.get().strip()
        if msg:
            self.controller.send_message(msg)
            self.message_entry.delete(0, tk.END)

    def send_message_event(self, event):
        self.send_message()

    def on_close(self):
        self.controller.stop()
        self.destroy()
