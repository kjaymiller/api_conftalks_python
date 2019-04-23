import responder

api = responder.API()

@api.route("/")
def test(req, resp):
    resp.text = 'Hello from Conftalks'

@api.route("/conferences/{conference_ID}")
def conferences(req, resp, *, conference_ID):
    resp.text = "Lookin' for some conferences?"

if __name__ == '__main__':
    api.run()
