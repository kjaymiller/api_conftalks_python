from mongo import (
        get_db_object_by_id,
        get_all_items
        )
import json
import responder

api = responder.API()

@api.route("/")
def test(req, resp):
    resp.text = 'Hello from Conftalks'

@api.route('/conferences')
def all_conferences(req, resp):
    resp.media = json.loads(get_all_items('conferences'))

@api.route("/conferences/{conference_Id}")
def conference_by_id(req, resp, *, conference_Id):
    conference_data = get_db_object_by_id('conferences', conference_Id) 
    resp.media = conference_data

if __name__ == '__main__':
    api.run()
