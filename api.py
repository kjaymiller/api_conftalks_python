from mongo import (
        db,
        get_db_data,
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

@api.route(before_request=True)
def auth_required(req, resp, user_data={}):
    api_key = {'api_key': req.headers.get('authorization')}
    if api_key:
        user_data = get_db_data('users', filter_by=api_key, return_one=True)
        req.headers.update({'user_data': user_data})


@api.schema('Event')
class EventSchema(Schema):
    id = fields.Str(attribute="_id.$oid")
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
    id = fields.Str(attribute="_id.$oid", data_key="_id.$oid")
    url = fields.Str()
    name = fields.Str()
    subscribed = fields.Boolean()


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
    conference_data = get_db_data('conferences')
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
        conference_data = get_db_data('conferences', _id=insert_id)
        conferences = ConferenceSchema()
        resp.media = conferences.dump(conference_data).data

    async def on_put(self, req, resp, *, conference_id):
        """Updates an Existing Conference Item"""
        api_key = req.headers['Authorization']
        request_media = await req.media(format='json')
        resp.media = get_db_data('conferences', _id=insert_id)

    def on_get(self, req, resp, *, conference_id):
        """Returns a single conference item""" 
        conference_data = get_db_data('conferences', _id=conference_id)

        if conference_data.get('subscribed_users'):
            conference_data['subscribed'] = req.headers['user_data']['email'] in conference_data['subscribed_users']
        
        else: 
            conference_data['subscribed'] = False

        conferences = ConferenceSchema().dump(conference_data)
        resp.media = conferences.data


@api.route('/subscribe/conference/{conference_id}')
class SubscribeToConference:
    """
    Subscribe Data
    ---
    put:
        description: Adds your email to the conference subscription list. This means that you       will recieve all notifications for this event. If you only want some of the notifications, look at /subscribe/event/{event_id}
        responses:
            200:
                description: Success (email was added)
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/Conference'
    """
    def on_put(self, req, resp, *, conference_id):
        data={'$push': {'subscribed_users': req.headers['user_data']['email']}}
        response = update_db_data('conferences', data=data, _id=conference_id)
        response['subscribed'] = True
        resp.media = ConferenceSchema().dump(response).data


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
        event_data = EventSchema().dump(get_db_data('events'))
        resp.media = event_data.data

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
        resp.media = EventSchema().dump(get_db_data('events', _id=response['$oid'])).data


@api.route("/user")
class User(req, resp):
    """Creates, or Retrieves User Data"""

    def confirmation_email(self, data):
        """sends confirmation email via mailgun"""
        send_confirmation_email(data) 

    async def on_post(self, req, resp):
        """Creates User Account"""
        request_media = await req.media(format='json')
        email_address = request_media['email']

        if not(get_db_data('users', filter_by={'email': email_address})): 
            api_key = generate_api_key()
            request_media['api_key'] = api_key
            insert_id = load_db_data('users', request_media)['$oid']
            resp.media = get_db_data('users', _id=insert_id)
            self.confirmation_email(resp.media[0])    
        
        else:
            resp.text = f'Email Account {email_address} already exists'
            resp.status_code = 400

    def on_get(self, req, resp):
        """Uses your api key to retrieve your user information."""
        resp.media = get_db_data('users', filter_by={'api_key':req.headers['Authorization']}) 


    async def on_put(self, req, resp):
        """Updates Your User Account"""
        request_media = await req.media(format='json')
        resp.media = update_db_data('users', filter_by=req.headers['user_data'], data=data)

@api.route('/event/{event_id}')
def get_event_by_id(req, resp, *, event_id):
    response = get_db_data('events', _id=event_id)
    response['subscribed'] = req.headers['user_data']['email'] in response.get('subscribed_users', [])
    event_data = EventSchema().dump(response).data
    resp.media=event_data
    

@api.route('/subscribe/event/{event_id}')
class UserSubcribeToEvent:
    """
    ---
    put:
        description: | 
            # Subscribes a user to an event.
            _reminder_times_ are calculated based on the ORIGINAL time.


            ```
            # equates to 1 day AFTER the start_date
            'start_reminder': {
                'interval': 'days', # or 'weeks'
                'amount': 1,
                } 
            ```

            optional 2nd/3rd reminders are based off the original date and not previous alerts. 
            If no _second_/_third_start_reminder_ is given, those reminders will be omitted.
             
            ```
            # equates to 2 weeks from the ORIGINAL Start Date
            'second_start_reminder': {
                'interval': 'weeks', 
                'amount': 2,
                }, 
            ```

            # End Date reminders work the same way but SUBTRACT From the end date

            ``` 
            # equates to 1 day BEFORE the end date.
            'end_reminder': {
                'interval': 'days', # or 'weeks'
                'amount': 1,
                }, 
            ```

            optional 2nd/3rd reminders are based off the original date and not previous alerts. 
            If no second/third_start_reminder, it will be omitted.

            ```
            # equates to 2 weeks from the ORIGINAL Date
            'second_start_reminder': {
                'interval': 'weeks', 
                'amount': 2,
                }, 

        responses:
            200:
                description: Success - Adds user to subscribed list
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/Event'
    """

    async def on_put(self, req, resp, *, event_id):
        request_media = await req.media(format="json")
        event_data = get_db_data('events', _id=event_id)
        start_date = maya.when(event_data['start_date']['$date']).datetime()
        start_reminders = [start_date]
        for reminder in request_media.get('start_reminders', []):
            days =  reminder['amount'] if reminder['interval'] == 'days' else 0 
            weeks = reminder['amount'] if reminder['interval'] == 'weeks' else 0
            start_reminders.append(maya.when(start_date).add(days=days, weeks=weeks).datetime())

        end_date = maya.when(event_data['end_date']['$date']).datetime()
        end_reminders = [end_date]
        for reminder in request_media.get('end_reminders', []):
            days =  reminder['amount'] if reminder['interval'] == 'days' else 0 
            weeks = reminder['amount'] if reminder['interval'] == 'weeks' else 0
            start_reminders.append(maya.when(end_date).sub(days=days, weeks=weeks).datetime())

        response_data={'$addToSet': 
                {'subscribers': 
                    {req.headers['user_data']['email']: 
                        {"start_reminders": start_reminders,
                            "end_reminders": end_reminders,
                            }
                        }
                    }
                }

        response = update_db_data(
                'events',
                _id=event_id,
                data=response_data,
                )

        resp.media = EventSchema().dump(response).data

        
@api.route("/user/api_regen")
async def regen_api_key(req, resp):
    if 'authorization_key' in req.params:
        data = get_db_data('users', filter_by={'api_reset.key': req.params['authorization_key']})
        resp.media = data

    elif 'email' in req.params:
        email = req.params['email']
        data = get_db_data('users', filter_by={'email': email})
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
