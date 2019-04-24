import secrets

def generate_api_key(len=20):
    return secrets.token_urlsafe(len)

