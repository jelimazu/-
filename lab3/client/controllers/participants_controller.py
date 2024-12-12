from tkinter import simpledialog, messagebox
from client.views.participants_view import ParticipantsView
from client.grpc_client import GrpcClient

class ParticipantsController:
    def __init__(self, meeting_id):
        self.meeting_id = meeting_id
        self.grpc_client = GrpcClient()
        self.view = ParticipantsView(self)
        self.update_participants()

    def update_participants(self):
        response = self.grpc_client.list_participants(self.meeting_id)
        participants = [{"id": p.participant_id, "name": p.name} for p in response.participants]
        self.view.update_participant_list(participants)

    def add_participant(self):
        name = simpledialog.askstring("Add Participant", "Enter participant name:")
        if not name:
            return
        response = self.grpc_client.add_participant(self.meeting_id, name)
        if response.success:
            messagebox.showinfo("Success", f"Participant '{name}' added.")
            self.update_participants()
        else:
            messagebox.showerror("Error", "Failed to add participant.")
