from markdown import markdown
from jinja2 import Template
from pathlib import Path

import requests
import os
import re
import json


def email_templates(filename, markdown='.md', text='.txt', **kwargs):
    templates = {} 
    
    for extension in (markdown, text):
        file_path = Path(f"{os['MAIL_TEMPLATES_DIR']}/{filename}{extension}")

        if file_path.isfile():
            template = Template(file_path.open().read())
            
            if file_path.suffix() == '.md':
                template[extension] = Markdown(template.render(**kwargs))
            
            else:
                template[extension] = template.render(**kwargs)

    return templates

def sendMessage(
        to,
        FROM,
        subject,
        emails,
        API_KEY=os.environ['MAILGUN_API_KEY'],
        url=os.environ['MAILGUN_URL'],
        tags=[],
        tracking=True,
        *args,
        ):

    recipient_variables = {}
    for user in to:
        {user['email'] = {key: user[key] for key in args}}

    email_data = {
        'to': to,
        'from': FROM['email'],
        'subject': subject,
        'text': emails['.txt'],
        'html': emails['.md'],
        'tracking': tracking,
        'recipient-variables': json.dumps(recipient_variables),
        'o:tag': tags,
        }

    return requests.post(
            url,
            auth=('api', API_KEY), 
            data=email_data,
            )
                

# Authentication
def send_confirmation_email(to, api_key):
    subject = 'Welcome to Conftalks - Your Conftalks API Key'

    return sendMessage( 
            to=to,
            subject=subject,
            emails = email_templates('email_notification', api_key=api_key),
            tags=['reminder', 'event'],
            ).sendMessage()


def send_event_email(to, conference, event, reminder):
    subject = f'conference'

    return mailGunEmailData( 
            to=to,
            subject=subject,
            emails = email_templates(
                    'email_notification',
                    conference=conference,
                    event=event, 
                    reminder=reminder,
                    ),
            text=emails['.txt'],
            html=emails['.md'],
            tags=['reminder', 'event'],
            ).sendMessage()


def send_reset_key_email(to, reset_key):
    subject = 'Reset your api key - Conftalks.dev' 
    
    return mailGunEmailData( 
            to=to,
            subject=subject,
            emails = email_template(
                    'reset_key_request_email',
                    expiration=reset_key['expiration'],
                    reset_link=os.environ['RESET_LINK'], 
                    authorization_key=reset_key['key'],
                    ),
            tags=['api_key', 'reset', 'confirmation'],
            ).sendMessage()
