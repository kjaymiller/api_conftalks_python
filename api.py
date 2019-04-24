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
async def all_conferences(req, resp):
    if req.method in ('post', 'put'):
        request_media = await req.media(format='json')
        insert_id = load_db_data('conferences', request_media)['$oid']
        resp.media = get_db_items('conferences', _id=insert_id)

    else:
        resp.media = get_db_items('conferences')

@api.route("/conferences/{conference_id}")
def conference_by_id(req, resp, *, conference_id):
        resp.media = get_db_items('conferences', _id=conference_id) 

if __name__ == '__main__':
    api.run()
