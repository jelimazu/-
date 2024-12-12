import grpc
from concurrent import futures
import datetime

import meeting_service_pb2
import meeting_service_pb2_grpc

from server.app import create_app, db
from server.app.models import Meeting, Participant

class MeetingServiceServicer(meeting_service_pb2_grpc.MeetingServiceServicer):
    def GetMeeting(self, request, context):
        # Оскільки ми працюємо всередині додатку Flask, потрібен app_context
        with app.app_context():
            meeting = Meeting.query.filter_by(id=request.meeting_id).first()
            if meeting:
                return meeting_service_pb2.GetMeetingResponse(
                    meeting_id=meeting.id,
                    title=meeting.title,
                    description=meeting.description if meeting.description else "",
                    date=meeting.date.isoformat()
                )
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Meeting not found")
                return meeting_service_pb2.GetMeetingResponse()

    def AddParticipant(self, request, context):
        with app.app_context():
            meeting = Meeting.query.filter_by(id=request.meeting_id).first()
            if not meeting:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Meeting not found")
                return meeting_service_pb2.AddParticipantResponse(success=False)

            new_participant = Participant(meeting_id=request.meeting_id, name=request.participant_name)
            db.session.add(new_participant)
            db.session.commit()
            return meeting_service_pb2.AddParticipantResponse(success=True)

    def ListParticipants(self, request, context):
        with app.app_context():
            participants = Participant.query.filter_by(meeting_id=request.meeting_id).all()
            response = meeting_service_pb2.ListParticipantsResponse()
            for p in participants:
                response.participants.add(participant_id=p.id, name=p.name)
            return response


def serve():
    # Створюємо Flask app та пушимо контекст
    global app
    app = create_app()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    meeting_service_pb2_grpc.add_MeetingServiceServicer_to_server(MeetingServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server running on port 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
