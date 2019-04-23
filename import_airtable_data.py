import requests
import maya
import bson
from datetime import datetime
from config import AIRTABLE_URL, AIRTABLE_KEY


url = AIRTABLE_URL

headers = {'Authorization': f'Bearer {AIRTABLE_KEY}'}

r = requests.get(url, headers=headers)
if not(r.raise_for_status()):
    conferences = r.json()['records']

entries = []

for record in conferences:
    entries.append({
            'url': record['fields'].get('conferenceURL', ''),
            'addedBy': record['fields'].get('addedBy', ''),
            'name': record['fields'].get('conferenceName', ''),
            'date_added': maya.when(record['fields'].get('creationDate',
                maya.now()))
            } )
print (entries)
