import falcon

class conferenceResource:
    def on_get(self, req, resp):
        resp.media = {'text': 'Hello from Conftalks'}

api = falcon.API()
api.add_route('/quote', conferenceResource())
        
