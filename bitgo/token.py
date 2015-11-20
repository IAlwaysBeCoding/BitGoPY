
__all__ = ['BitGoAccessToken']

class BitGoAccessToken(object):

    """
        This BitGoAccessToken class for now
        will just contain the access_token
        internall inside the 'token' property.
        In the future, its API may change.
    """
    def __init__(self,access_token):
        self.token = access_token
