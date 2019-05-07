from mongo import (
        db,
        get_db_items,
        load_db_data,
        update_db_data,
        )

from marshmallow import Schema, fields

from mail import (
        send_confirmation_email,
        send_reset_key_email,
        )

from key_gen import generate_api_key
import json
import responder
import maya

contact = {
        'name': 'Productivity in Tech',
        'url': 'https://productivityintech.com',
        'email': 'info@productivityintech.com',
        }

api_description = '''This is the Conftalks.dev Public API. It is used to manage
your alerts!
'''
        

api = responder.API(
        title='Conftalks API',
        version='0.1',
        openapi='3.0.2',
        docs_route='/',
        contact=contact,
        description=api_description,
        )

@api.schema('Event')
class EventSchema(Schema):
    id = fields.Str(attribute="_id.$oid")
    conference = fields.Str()
    url = fields.Str()
    name = fields.Str()
    start_date = fields.Str(attribute="start_date.$date")
    end_date = fields.Str(attribute="end_date.$date")


@api.schema('Conference')
class ConferenceSchema(Schema):
    id = fields.Str(attribute="_id.$oid", data_key="_id.$oid")
    url = fields.Str()
    name = fields.Str()

@api.route("/conferences")
def conferences(req, resp):
    """
    TODO: Add Filters
    ---
    get:
        description: Returns a list of the Conferences in the system
        responses:
            200:
                description: Success
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/Conference'
    """
    conference_data = get_db_items('conferences')
    conferences = ConferenceSchema(many=True)
    resp.media = conferences.dump(conference_data).data


@api.route('/conferences/{conference_id}')
class ConferenceById:
    """
    ---
    get: 
        description: Return the information on a single conference.
        responses:
            200:
                description: Success
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/Conference'

    post:
        description: Add a new conference.
        responses:
            200:
                description: Success
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/Conference'

    put:
        description: Update an existing conference.
        responses:
            200:
                description: Success
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/Conference'
    """
    async def on_post(self, req, resp, *, conference_id):
        """Creates New Conference Item"""
        request_media = await req.media(format='json')
        insert_id = load_db_data('conferences', request_media)
        conference_data = get_db_items('conferences', _id=insert_id)
        conferences = ConferenceSchema()
        resp.media = conferences.dump(conference_data).data


    async def on_put(self, req, resp, *, conference_id):
        """Updates an Existing Conference Item"""
        request_media = await req.media(format='json')
        resp.media = get_db_items('conferences', _id=insert_id)

    def on_get(self, req, resp, *, conference_id):
        """Returns a single conference item""" 
        conference_data = get_db_items('conferences', _id=conference_id)
        conferences = ConferenceSchema().dump(conference_data)
        resp.media = conferences.data


@api.route('/event')
class Events:
    """
    ---
    get:
        description: Returns a Single Event Object
        responses:
            200:
                description: Success 
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/Event'

    post:
        description: Creates a Single Event
        responses:
            200:
                description: Success 
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/Event'
    """

    def on_get(self, req, resp):
        """Return Latest Events Limited by Limit Request.
        TODO: Restrict calls not using a filter.
        """
        event_data = EventSchema(get_db_items('events'))
        resp.media = event_data

    async def on_post(self, req, resp):
        """Add an event to the events collection.
        TODO: Bulk Add Events.
        TODO: Lock Update with API_KEY.
        If the event exists the content will be overridden.
        """

        request_media = await req.media(format='json')
        
        #convert start and end dates to datetime
        request_media['start_date'] = maya.when(request_media['start_date']).datetime()
        request_media['end_date'] = maya.when(request_media['end_date']).datetime()
        response = load_db_data('events', request_media)
        resp.media = EventSchema().dump(get_db_items('events', _id=response['$oid'])).data


@api.route("/user")
async def User(req, resp):
    """Creates, or Retrieves User Data"""

    def confirmation_email(self, data):
        """sends confirmation email via mailgun"""
        send_confirmation_email(data) 

    async def on_post(self, req, resp):
        """Creates User Account"""
        request_media = await req.media(format='json')
        email_address = request_media['email']

        if not(get_db_items('users', filter_by={'email': email_address})): 
            api_key = generate_api_key()
            request_media['api_key'] = api_key
            insert_id = load_db_data('users', request_media)['$oid']
            resp.media = get_db_items('users', _id=insert_id)
            self.confirmation_email(resp.media[0])    
        
        else:
            resp.text = f'Email Account {email_address} already exists'
            resp.status_code = 400

    def on_get(self, req, resp):
        """Uses your api key to retrieve your user information."""
        resp.media = get_db_items('users', filter_by={'api_key':req.headers['Authorization']}) 


@api.route('/event/{event_id}')
def get_event_by_id(req, resp, *, event_id):
    resp.media = get_db_items('events', _id=event_id)

@api.route('/event/{event_id}/subscribe')
class UserSubcribeToEvent:
    async def on_post(self, req, resp, *, event_id):
        user_info = get_db_items(
                'users', 
                filter_by={'api_key': req.headers['Authorization']})[0]

        subscription_data = await req.media(format='json')
        resp.media = update_db_data(
                'events',
                _id=event_id,
                data={'$push': {'subscribers': {user_info['email']: subscription_data}}})

        
@api.route("/user/api_regen")
async def regen_api_key(req, resp):
    if 'authorization_key' in req.params:
        data = get_db_items('users', filter_by={'api_reset.key': req.params['authorization_key']})
        resp.media = data

    elif 'email' in req.params:
        email = req.params['email']
        data = get_db_items('users', filter_by={'email': email})
        reset_key = update_db_data(
                'users', 
                filter_by={'email': email},
                data={'$set': {'api_reset': {'key': generate_api_key(35),
                    'expiration': maya.now().add(minutes=5).datetime()}}},
                )['api_reset']

        @api.background.task
        def key_reset():
            send_reset_key_email(to=email, reset_key=reset_key)
            
        await key_reset()
        resp.text = 'An email with your Reset Key will be sent to you!'

    else: 
        resp.status_code = 400
        resp.text = 'You must supply an email or an authorization_key'


if __name__ == '__main__':
    api.run()
