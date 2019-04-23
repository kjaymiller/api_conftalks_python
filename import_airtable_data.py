import requests
import maya
from mongo import conferences as conferences_collection
from datetime import datetime
from config import MLAB_DB, AIRTABLE_URL, AIRTABLE_KEY


url = AIRTABLE_URL

headers = {'Authorization': f'Bearer {AIRTABLE_KEY}'}

r = requests.get(url, headers=headers)
if not(r.raise_for_status()):
    conferences = r.json()['records']


def get_maya_time(time):
    if time:
        t = maya.when(time)

    else:
        t = maya.now()
    return t.rfc3339()

def main():
    entries = []
    for record in conferences:
        r = record['fields']
        entries.append({
            'url': r.get('conferenceURL', ''),
            'addedBy': r.get('addedBy', ''),
            'name': r.get('conferenceName', ''),
            'date_added': get_maya_time(r.get('createdTime')),
            } )

    return conferences_collection.insert_many(entries)

if __name__ == '__main__':
    main()
