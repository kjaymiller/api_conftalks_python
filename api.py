from mongo import (
        get_db_items,
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

api = responder.API()

@api.route("/")
def test(req, resp):
    resp.text = 'Hello from Conftalks'

@api.route('/conferences')
async def all_conferences(req, resp):
    if req.method in ('post', 'put'):
        request_media = await req.media(format='json')
        insert_id = load_db_data('conferences', request_media)['$oid']
        resp.media = get_db_items('conferences', _id=insert_id)

    else:
        resp.media = get_db_items('conferences')

@api.route("/conferences/{conference_id}")
def conference_by_id(req, resp, *, conference_id):
    resp.media = get_db_items('conferences', _id=conference_id) 


@api.route("/user")
async def add_user(req, resp):

    @api.background.task
    def confirmation_email(data):
        send_confirmation_email(data) 
    
    if req.method == 'post':
        request_media = await req.media(format='json')
        email_address = request_media['email']

        if not(get_db_items('users', filter_by={'email': email_address})): 
            api_key = generate_api_key()
            request_media['api_key'] = api_key
            insert_id = load_db_data('users', request_media)['$oid']
            resp.media = get_db_items('users', _id=insert_id)
            confirmation_email(resp.media[0])    
        
        else:
            resp.text = f'Email Account {email_address} already exists'
            resp.status_code = 400

    elif req.headers['Authorization']:
        resp.media = get_db_items('users', filter_by={'api_key':req.headers['Authorization']})

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
                    'expiration': maya.now().add(minutes=5).rfc2822()}}},
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
