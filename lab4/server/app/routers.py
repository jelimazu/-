from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource, fields
from .models import db, Meeting

# Blueprint для Flask-RESTX
bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(bp, title="Meeting Management API", version="1.0", description="API для управління зустрічами")

# Модель для Swagger
meeting_model = api.model('Meeting', {
    'id': fields.Integer(readOnly=True, description='Унікальний ідентифікатор зустрічі'),
    'title': fields.String(required=True, description='Назва зустрічі'),
    'description': fields.String(description='Опис зустрічі'),
    'date': fields.String(required=True, description='Дата зустрічі в ISO форматі')
})

@api.route('/meetings')
class MeetingListResource(Resource):
    @api.doc('list_meetings')
    @api.marshal_list_with(meeting_model)
    def get(self):
        """Отримати список усіх зустрічей"""
        meetings = Meeting.query.all()
        return [meeting.to_dict() for meeting in meetings]

    @api.doc('create_meeting')
    @api.expect(meeting_model)
    @api.marshal_with(meeting_model, code=201)
    def post(self):
        """Створити нову зустріч"""
        data = request.json
        meeting = Meeting(
            title=data['title'],
            description=data.get('description'),
            date=data['date']
        )
        db.session.add(meeting)
        db.session.commit()
        return meeting.to_dict(), 201

@api.route('/meetings/<int:id>')
class MeetingResource(Resource):
    @api.doc('get_meeting')
    @api.marshal_with(meeting_model)
    def get(self, id):
        """Отримати інформацію про одну зустріч"""
        meeting = Meeting.query.get_or_404(id)
        return meeting.to_dict()

    @api.doc('update_meeting')
    @api.expect(meeting_model)
    @api.marshal_with(meeting_model)
    def put(self, id):
        """Оновити інформацію про зустріч"""
        meeting = Meeting.query.get_or_404(id)
        data = request.json
        meeting.title = data.get('title', meeting.title)
        meeting.description = data.get('description', meeting.description)
        meeting.date = data.get('date', meeting.date)
        db.session.commit()
        return meeting.to_dict()

    @api.doc('delete_meeting')
    def delete(self, id):
        """Видалити зустріч"""
        meeting = Meeting.query.get_or_404(id)
        db.session.delete(meeting)
        db.session.commit()
        return '', 204
