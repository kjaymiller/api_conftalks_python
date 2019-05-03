from markdown import markdown
from jinja2 import Template
from pathlib import Path

import requests
import os
import re
from dataclasses import dataclass, field


def email_templates(filename, markdown='.md', text='.txt'):
    templates = {} 
    for extension in (markdown, text)
        file_path = Path(f"{os['MAIL_TEMPLATES_DIR']}/{filename}{extension}")
        if file_path.isfile():
            templates[extension] = (file_path.read())
        )

    return templates


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


def send_reset_key_email(to, conference, event, reminder):
    subject = 'Reset your api key - Conftalks.dev' 
    emails = {}
    
    for base_template in email_templates('email_notification'):
        template = Template(base_template['base_template']) 
        emails[base_template] = template.render(
                conference=conference,
                event=event, 
                reminder=reminder,
                )

    return mailGunEmailData( 
            to=to,
            subject=subject,
            text=emails['.txt'],
            html=Markdown(emails['.md']),
            tags=['reminder', 'event'],
            ).sendMessage())
