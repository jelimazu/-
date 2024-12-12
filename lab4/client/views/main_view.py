import tkinter as tk
from tkinter import ttk

class MainView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Meeting Manager")
        self.geometry("600x400")

        self.meeting_list = ttk.Treeview(self, columns=("ID", "Title", "Date"), show="headings")
        self.meeting_list.heading("ID", text="ID")
        self.meeting_list.heading("Title", text="Title")
        self.meeting_list.heading("Date", text="Date")
        self.meeting_list.pack(fill=tk.BOTH, expand=True)

        self.add_button = tk.Button(self, text="Add Meeting", command=self.controller.add_meeting)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.edit_button = tk.Button(self, text="Edit Meeting", command=self.controller.edit_meeting)
        self.edit_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = tk.Button(self, text="Delete Meeting", command=self.controller.delete_meeting)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.chat_button = tk.Button(self, text="Open Chat", command=self.controller.open_chat)
        self.chat_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.participants_button = tk.Button(self, text="Manage Participants", command=self.controller.manage_participants)
        self.participants_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.view_tags_button = tk.Button(self, text="View Tags", command=self.controller.view_tags)
        self.view_tags_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_tag_button = tk.Button(self, text="Add Tag", command=self.controller.add_tag)
        self.add_tag_button.pack(side=tk.LEFT, padx=5, pady=5)

    def update_meeting_list(self, meetings):
        for row in self.meeting_list.get_children():
            self.meeting_list.delete(row)
        for meeting in meetings:
            self.meeting_list.insert("", "end", values=(meeting["id"], meeting["title"], meeting["date"]))
