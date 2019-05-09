from api import api
from mongo import (
        db,
        get_db_data,
        load_db_data,
        update_db_data,
        )
from schemas import ConferenceSchema


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

