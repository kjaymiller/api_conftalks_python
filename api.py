from mongo import (
        db,
        get_db_data,
        load_db_data,
        update_db_data,
        )

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


if __name__ == '__main__': 
    from events import *
    from users import *
    from conferences import *
    api.run()
