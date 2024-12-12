import grpc
import meeting_service_pb2
import meeting_service_pb2_grpc

class GrpcClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = meeting_service_pb2_grpc.MeetingServiceStub(self.channel)

    def get_meeting(self, meeting_id):
        request = meeting_service_pb2.GetMeetingRequest(meeting_id=meeting_id)
        return self.stub.GetMeeting(request)

    def add_participant(self, meeting_id, participant_name):
        request = meeting_service_pb2.AddParticipantRequest(
            meeting_id=meeting_id, participant_name=participant_name
        )
        return self.stub.AddParticipant(request)

    def list_participants(self, meeting_id):
        request = meeting_service_pb2.ListParticipantsRequest(meeting_id=meeting_id)
        return self.stub.ListParticipants(request)
