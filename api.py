import responder

api = responder.API()

@api.route("/")
def test(req, resp):
    resp.text = 'Hello from Conftalks'

 __name__ == '__main__':
    api.run()
