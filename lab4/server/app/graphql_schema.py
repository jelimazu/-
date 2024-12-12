import graphene
from graphene import ObjectType, String, Field, Int, List, Boolean
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from server.app.models import db, Meeting, Tag


class TagType(SQLAlchemyObjectType):
    class Meta:
        model = Tag
        interfaces = (graphene.relay.Node, )

class MeetingType(SQLAlchemyObjectType):
    class Meta:
        model = Meeting
        interfaces = (graphene.relay.Node, )
    tags = List(TagType)

    def resolve_tags(parent, info):
        return parent.tags

class Query(ObjectType):
    meeting = Field(MeetingType, id=Int(required=True))
    meetings = List(MeetingType)

    def resolve_meeting(self, info, id):
        return Meeting.query.filter_by(id=id).first()

    def resolve_meetings(self, info):
        return Meeting.query.all()

class AddTagToMeeting(graphene.Mutation):
    class Arguments:
        meeting_id = Int(required=True)
        name = String(required=True)

    success = Boolean()

    def mutate(self, info, meeting_id, name):
        meeting = Meeting.query.filter_by(id=meeting_id).first()
        if not meeting:
            return AddTagToMeeting(success=False)
        new_tag = Tag(meeting_id=meeting_id, name=name)
        db.session.add(new_tag)
        db.session.commit()
        return AddTagToMeeting(success=True)

class Mutation(ObjectType):
    add_tag_to_meeting = AddTagToMeeting.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
