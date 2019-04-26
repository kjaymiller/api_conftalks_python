from markdown import markdown

import requests
import os
import re
from dataclasses import dataclass, field

@dataclass
class mailGunEmailData:
    to: str
    subject: str
    text: str
    html: str
    url: str = os.environ['MAILGUN_URL']
    tags: list = field(default_factory=list) 
    API_KEY: str = os.environ['MAILGUN_API_KEY']
    FROM: str = os.environ['MAILGUN_ADMIN_EMAIL']
    tracking: bool = True
    
    def mail_gun_email_data(self):
        return {
            'to': self.to,
            'from': self.FROM,
            'subject': self.subject,
            'text': self.text,
            'html': self.html,
            'tracking': self.tracking,
            'o:tag': self.tags,
            }

    def sendMessage(self):
        return requests.post(
                self.url,
                auth=('api', self.API_KEY), 
                data=self.mail_gun_email_data())
                


# Authentication
def send_confirmation_email(to, api_key):
    subject = 'Welcome to Conftalks - Your Conftalks API Key'
    with open('./email_templates/confirmation_email.md') as md_file:
        raw_markdown = md_file.read()
        md_email = re.sub(r'{{API_KEY}}', api_key, raw_markdown)
        html = markdown(md_email)

    with open('./email_templates/confirmation_email.txt') as txt_email:
        raw_text = txt_email.read()
        text = re.sub(r'{{API_KEY}}', api_key, raw_text)

    print(mailGunEmailData( 
            to=to,
            subject=subject,
            text=text,
            html=html,
            tags=['api_key', 'confirmation'],
            ).sendMessage().url)


def send_reset_key_email(to, reset_key):
    subject = 'Reset your api key - Conftalks.dev' 
    with open('./email_templates/reset_key_request_email.md') as md_file:
        raw_markdown = md_file.read()
        md_email = re.sub(r'{{EXPIRATION}}', reset_key['expiration'], raw_markdown)
        md_email = re.sub(r'{{RESET_LINK}}', os.environ['RESET_LINK'], md_email)
        md_email = re.sub(r'{{AUTHORIZATION_KEY}}', reset_key['key'], md_email)
        html = markdown(md_email)

    with open('./email_templates/reset_key_request_email.txt') as txt_email:
        raw_text = txt_email.read()
        text = re.sub(r'{{EXPIRATION}}', reset_key['expiration'], raw_text)
        text = re.sub(r'{{RESET_LINK}}', os.environ['RESET_LINK'], text)
        text = re.sub(r'{{AUTHORIZATION_KEY}}', reset_key['key'], text)

    print(mailGunEmailData( 
            to=to,
            subject=subject,
            text=text,
            html=html,
            tags=['api_key', 'reset', 'confirmation'],
            ).sendMessage())
