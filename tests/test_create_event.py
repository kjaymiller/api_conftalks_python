import requests
import maya
import json

def create_db_entry():
    data = {
            'title': 'Test CFP Event',
            'start_date': maya.now().rfc2822(),
            'end_date': maya.now().add(days=1).rfc2822(),
            'conference_id':  '5cbfa011127c6adabe9bfcb3',
            }
    return requests.post('http://localhost:5042/event', data=data)
    

if __name__ == "__main__":
    r = create_db_entry()
    print(r)
