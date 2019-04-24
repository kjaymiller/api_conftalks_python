from markdown import markdown

import requests
import os
import re

MAILGUN_BASE_URL = os.environ['MAILGUN_URL']
API_KEY = os.environ['MAILGUN_API_KEY']

# Authentication
def send_confirmation_email(data):
    TO = data['email']
    FROM = os.environ['MAILGUN_ADMIN_EMAIL']
    SUBJECT = 'Welcome to Conftalks'
    with open('./confirmation_email.md') as md_file:
        raw_markdown = md_file.read()
        md_email = re.sub(r'{{API_KEY}}', data['api_key'], raw_markdown)
        html_email = markdown(md_email)

    with open('./confirmation_email.txt') as txt_email:
        raw_text = txt_email.read()
        text_email = re.sub(r'{{API_KEY}}', data['api_key'], raw_text)

    data = {
            'to': TO,
            'from': FROM,
            'subject': SUBJECT,
            'text': text_email,
            'html': html_email,
            'tracking': True,
            'o:tag': ['api_key', 'confirmation'],
            }

    print(requests.post(f'{MAILGUN_BASE_URL}/messages', auth=('api', API_KEY), data=data).text)
