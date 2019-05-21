from api import api
from marshmallow import Schema, fields


@api.schema('Event')
class EventSchema(Schema):
    id = fields.Str(attribute=str('_id'))
    conference = fields.Str()
    url = fields.Str()
    name = fields.Str()
    start_date = fields.Str(attribute="start_date.$date")
    start_reminders = fields.List(fields.String)
    end_date = fields.Str(attribute="end_date.$date")
    end_reminders = fields.List(fields.String)
    subscribed = fields.Boolean()


@api.schema('Conference')
class ConferenceSchema(Schema):
    id = fields.Function(lambda obj: str(obj['id']))
    url = fields.Str()
    name = fields.Str()
    subscribed = fields.Boolean()
    event_start = fields.Str()
    event_end = fields.Str()


@api.schema('User')
class UserSchema(Schema):
    id = fields.Str(attribute="_id.$oid")
    name = fields.Str()
    subscribed_conferences = fields.List(fields.String)
    subscribed_events = fields.List(fields.String)
