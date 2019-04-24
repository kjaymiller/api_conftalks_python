from mongo import (
        get_db_items,
        load_db_data
        )

import json
import responder

api = responder.API()

@api.route("/")
def test(req, resp):
    resp.text = 'Hello from Conftalks'

@api.route('/conferences')
def all_conferences(req, resp):
    resp.media = get_db_items('conferences')

@api.route("/conferences/{conference_id}")
async def conference_by_id(req, resp, *, conference_id):
    if req.media:
        request_data = await req.media(format="json")
         

    resp.media = get_db_items('conferences', _id=conference_id) 

if __name__ == '__main__':
    api.run()
