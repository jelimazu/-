from . import db

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)

    participants = db.relationship("Participant", back_populates="meeting")
    tags = db.relationship("Tag", back_populates="meeting")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date": self.date.isoformat()
        }

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    meeting = db.relationship("Meeting", back_populates="participants")

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    meeting = db.relationship("Meeting", back_populates="tags")
