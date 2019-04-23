import requests
import maya
import bson
from datetime import datetime


url = 'https://api.airtable.com/v0/appuFBQpMhzKDXSHn/Conferences?view=Grid%20view'

headers = {'Authorization': 'Bearer keyOzyWXah5fdzUL1'}

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
