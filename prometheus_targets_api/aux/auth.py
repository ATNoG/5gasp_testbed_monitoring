import constants as Constants

def is_auth_token_valid(token):
    if token == Constants.AUTH_TOKEN:
        return True
    return False
