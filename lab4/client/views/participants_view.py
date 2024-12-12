import tkinter as tk
from tkinter import ttk

class ParticipantsView(tk.Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Participants Manager")
        self.geometry("400x300")

        # Список учасників
        self.participant_list = ttk.Treeview(self, columns=("ID", "Name"), show="headings")
        self.participant_list.heading("ID", text="ID")
        self.participant_list.heading("Name", text="Name")
        self.participant_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Кнопка додавання
        self.add_button = tk.Button(self, text="Add Participant", command=self.controller.add_participant)
        self.add_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Кнопка оновлення
        self.refresh_button = tk.Button(self, text="Refresh", command=self.controller.update_participants)
        self.refresh_button.pack(side=tk.LEFT, padx=10, pady=10)

    def update_participant_list(self, participants):
        for row in self.participant_list.get_children():
            self.participant_list.delete(row)
        for p in participants:
            self.participant_list.insert("", "end", values=(p["id"], p["name"]))
