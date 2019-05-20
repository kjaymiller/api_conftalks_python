from api import api
from mongo import (
        get_db_data,
        load_db_data,
        update_db_data,
        jsonify,
        )

from schemas import ConferenceSchema as Conference

collection = 'conferences'

def get_conference_data(*, _id:str='', filter_by:dict={}):
    """returns a single conference as a ConferenceSchema item"""
    
    if _id:
        conference_data = get_db_data(
            collection=collection,
            _id=_id,
            )
        many=False

    else:
        conference_data = get_db_data(
        collection=collection,
        filter_by=filter_by,
        )
        many=True
    
    return Conference(many=many).dump(conference_data)
            
@api.route("/conferences")
def conferences(req, resp):
    """
    TODO: Add Filter Support for Date Recognition
    TODO: Add Filter Support for Organizers
    TODO: Add Filter Support for Subscribed Events Only
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
    conference_data = get_conference_data(filter_by=req.media.get('filter', {}))
    resp.media = conference_data # TODO: Add Filter_By from Request Header


@api.route('/conferences/{conference_id}')
class ConferenceById:
    """
    ---
    get: 
        description: Return the information on a single conference.
        parameters:
            - in: path
              name: conference_id
              description: The id of the conference that you are wanting to load.
              schema:
                type: string
              required: true
            
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
        insert_id = load_db_data(collection='conferences', data=request_media)
        conference_data = get_db_data('conferences', _id=insert_id)
        conferences = ConferenceSchema()
        resp.media = conferences.dump(conference_data)

    async def on_put(self, req, resp, *, conference_id):
        """Updates an Existing Conference Item"""
        api_key = req.headers['Authorization']
        request_media = await req.media(format='json')
        resp.media = get_db_data(collection='conferences', _id=insert_id)

    def on_get(self, req, resp, *, conference_id):
        """Returns a single conference item""" 
        resp.media = get_conference_data(_id=conference_id)

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
        resp.media = ConferenceSchema().dump(response)

