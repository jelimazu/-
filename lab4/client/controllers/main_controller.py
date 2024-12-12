from datetime import datetime
from tkinter import simpledialog, messagebox
from client.controllers.chat_controller import ChatController
from client.controllers.participants_controller import ParticipantsController
from client.rest_client import RestClient
from client.views.main_view import MainView
from client.graphql_client import GraphQLClient

class MainController:
    def __init__(self):
        self.view = MainView(self)
        self.update_meetings()
        self.graphql_client = GraphQLClient()

    def update_meetings(self):
        meetings = RestClient.get_meetings()
        self.view.update_meeting_list(meetings)

    def add_meeting(self):
        title = simpledialog.askstring("Add Meeting", "Enter meeting title:")
        if not title:
            return
        while True:
            date = simpledialog.askstring("Add Meeting", "Enter new meeting date (YYYY-MM-DD):")
            try:
                datetime.strptime(date, "%Y-%m-%d")
                break
            except ValueError:
                messagebox.showwarning("Add Meeting", "Invalid date format. Please use YYYY-MM-DD.")
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

    def open_chat(self):
        selected_item = self.view.meeting_list.selection()
        if not selected_item:
            messagebox.showwarning("Open Chat", "No meeting selected.")
            return
        meeting_id = self.view.meeting_list.item(selected_item)["values"][0]
        ChatController(meeting_id)

    def manage_participants(self):
        selected_item = self.view.meeting_list.selection()
        if not selected_item:
            messagebox.showwarning("Manage Participants", "No meeting selected.")
            return
        meeting_id = self.view.meeting_list.item(selected_item)["values"][0]
        ParticipantsController(meeting_id)

    def view_tags(self):
        selected_item = self.view.meeting_list.selection()
        if not selected_item:
            messagebox.showwarning("View Tags", "No meeting selected.")
            return
        meeting_id = self.view.meeting_list.item(selected_item)["values"][0]
        result = self.graphql_client.query_meeting(meeting_id)
        data = result.get("data", {}).get("meeting", {})
        if not data:
            messagebox.showwarning("View Tags", "No meeting found.")
            return
        tags = data.get("tags", [])
        tag_names = ", ".join([t["name"] for t in tags]) if tags else "No tags"
        messagebox.showinfo("Tags", f"Meeting '{data['title']}' tags: {tag_names}")

    def add_tag(self):
        selected_item = self.view.meeting_list.selection()
        if not selected_item:
            messagebox.showwarning("Add Tag", "No meeting selected.")
            return
        meeting_id = self.view.meeting_list.item(selected_item)["values"][0]
        tag_name = simpledialog.askstring("Add Tag", "Enter tag name:")
        if not tag_name:
            return
        result = self.graphql_client.add_tag(meeting_id, tag_name)
        success = result.get("data", {}).get("addTagToMeeting", {}).get("success", False)
        if success:
            messagebox.showinfo("Add Tag", f"Tag '{tag_name}' added successfully.")
        else:
            messagebox.showerror("Add Tag", "Failed to add tag.")
