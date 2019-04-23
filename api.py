import responder

api = responder.API()

@api.route("/")
def conferences(req, resp):
    resp.text = 'Hello from Conftalks'

if __name__ == '__main__':
    api.run(port='443')
