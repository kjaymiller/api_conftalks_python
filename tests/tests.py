import requests
import json
import maya

url = 'http://localhost:5042/events'
event = {'event_name': 'cfp',
        'conference_id': '5cbfa011127c6adabe9bfcb3',
        'event_start': maya.now().rfc2822(),
        'event_end': maya.now().add(days=2).rfc2822()
        }

r = requests.post(url, data=json.dumps({'events':event}))
