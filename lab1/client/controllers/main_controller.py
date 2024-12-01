from datetime import datetime

from client.rest_client import RestClient
from client.views.main_view import MainView
from tkinter import simpledialog, messagebox

class MainController:
    def __init__(self):
        self.view = MainView(self)
        self.update_meetings()

    def update_meetings(self):
        meetings = RestClient.get_meetings()
        self.view.update_meeting_list(meetings)

    def add_meeting(self):
        title = simpledialog.askstring("Add Meeting", "Enter meeting title:")
        if not title:
            return
        while True:
            date = simpledialog.askstring("Edit Meeting", "Enter new meeting date (YYYY-MM-DD):")
            try:
                datetime.strptime(date, "%Y-%m-%d")
                break
            except ValueError:
                messagebox.showwarning("Edit Meeting", "Invalid date format. Please use YYYY-MM-DD.")
        data = {"title": title, "date": date}
        RestClient.create_meeting(data)
        self.update_meetings()

    def edit_meeting(self):
        selected_item = self.view.meeting_list.selection()
        if not selected_item:
            messagebox.showwarning("Edit Meeting", "No meeting selected.")
            return
        item_id = self.view.meeting_list.item(selected_item)["values"][0]
        title = simpledialog.askstring("Edit Meeting", "Enter new meeting title:")
        while True:
            date = simpledialog.askstring("Edit Meeting", "Enter new meeting date (YYYY-MM-DD):")
            try:
                datetime.strptime(date, "%Y-%m-%d")
                break
            except:
                messagebox.showwarning("Edit Meeting", "Invalid date format. Please use YYYY-MM-DD.")

        data = {"title": title, "date": date}
        RestClient.update_meeting(item_id, data)
        self.update_meetings()

    def delete_meeting(self):
        selected_item = self.view.meeting_list.selection()
        if not selected_item:
            messagebox.showwarning("Delete Meeting", "No meeting selected.")
            return
        item_id = self.view.meeting_list.item(selected_item)["values"][0]
        RestClient.delete_meeting(item_id)
        self.update_meetings()
