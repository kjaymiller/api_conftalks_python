from api import api
from pymongo import ASCENDING as pymongo_ASCENDING 
from pymongo import DESCENDING as pymongo_DESCENDING
from mongo import (
        db,
        get_db_data,
        load_db_data,
        update_db_data,
        )
from schemas import EventSchema

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


        user_update_data={'$addToSet': {'subscriptions': [event_id]}}
        update_db_data(
                'users', 
                filter_by=req.headers['user_data'],
                data=user_update_data,
                )

        resp.media = EventSchema().dump(response).data


@api.route('/event/{event_id}')
def get_event_by_id(req, resp, *, event_id):
    response = get_db_data('events', _id=event_id)
    response['subscribed'] = req.headers['user_data']['email'] in response.get('subscribed_users', [])
    event_data = EventSchema().dump(response).data
    resp.media=event_data
    

@api.route('/events')
def get_events(req, resp):
    """
    ---
    get:
        description: returns the events for the Authenticated User
        parameters:
            - in: query
              name: limit
              description: The **number of items** to return from the query
              schema:
                  type: integer 
                  default: 10

            - in: query
              name: sort_key
              description: Which _date parameter_ to use for filtering by.
              schema:
                type: string
                enum:
                    - start_date
                    - end_date
                default: start_date
        responses:
            200:
                description: Success 
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/Event'
    """
    sorting_options = {
           'ascending': pymongo_ASCENDING,
           'descending': pymongo_DESCENDING,
           }
    limit = req.params.get('limit', '10')
    sort_key = req.params.get('sort_key', 'start_date')
    sort_order = sorting_options[req.params.get('sort_order', 'descending')]
    sort = (sort_key, sort_order)
    filter_by = {}

    if req.params.get('conference') == 1:
        filter_by.update({'conference_id': req.params['conference']})
        limit = 0
    
    if req.params('subscribed') == 1:
        filter_by.update({'subscribers': req.headers['user_data']['email_address']})
        limit = 0

    events = get_db_data('events', filter_by=filter_by, sort=sort, limit=limit)
    resp.media = EventSchema(many=True).dump(events)
