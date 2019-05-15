from api import api
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
from schemas import UserSchema

@api.route("/user")
class User:
    """
    Creates, Updates or Retrieves User Data
    ---
    get:
        description: Returns the user data matching the api-key
        responses:
            200:
                security:
                    - APIKey: []
                content:
                    application/json:
                        schema: 
                            $ref: '#/components/schemas/User'
    """

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
            user_data = update_db_data('users', request_media, upsert=True)
            resp.media = UserSchema().dump(user_data)
            self.confirmation_email(resp.media[0])    

        
        else:
            resp.text = f'Email Account {email_address} already exists'
            resp.status_code = 400

    def on_get(self, req, resp):
        """Uses your api key to retrieve your user information."""
        print(req.headers)
        resp.media = UserSchema().dump(req.headers['user_data'])

    async def on_put(self, req, resp):
        """Updates Your User Account"""
        request_media = await req.media(format='json')
        resp.media = update_db_data('users', filter_by=req.headers['user_data'], data=data)

        
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


