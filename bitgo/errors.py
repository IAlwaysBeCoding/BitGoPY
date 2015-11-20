
__all__ = ['BitGoException','AccessTokenException','InvalidAccessToken',
           'BitGoClientException','InvalidClient','BitGoResourceException',
           'InvalidResourceEndpoint','InvalidResourceEndpointUrl','InvalidResourceMethod',
           'HttpError','BadRequest','Unauthorized','Forbidden','NotFound','NotAcceptable']


class BitGoException(Exception):
    """General BitGo's Exception"""
    pass


class AccessTokenException(BitGoException):
    """BitGo'exceptions related to access tokens"""
    pass


class InvalidAccessToken(AccessTokenException):
    """Invalid access token type.Raised when
        the access token provided is not a valid
        str or a BitGoAccessToken instance."""
    pass


class BitGoClientException(BitGoException):
    """BitGo's exceptions related to the client """
    pass


class InvalidClient(BitGoClientException):
    """ Invalid BitGo client instance """
    pass


class BitGoResourceException(BitGoException):
    """ BitGo's exceptions related to anything
        regarding a resource """
    pass


class InvalidResourceEndpoint(BitGoResourceException):
    """Raised when an invalid endpoint was found in
        inside the BitGoResource's class ENDPOINT
        variable that contains the mappings for all
        the resource's actions
    """
    pass


class InvalidResourceEndpointUrl(BitGoResourceException):

    """
        Raised when an invalid Endpoint url was found
        inside one of the ENDPOINT dictionary keys
    """
    pass


class InvalidResourceMethod(BitGoResourceException):

    """
        Raised when an invalid method was passed
        to be used for requesting a resource's endpoint
        could not be found.This happens when neither
        'GET','POST','PUT' or 'DELETE' was found as a valid
        http(s) method
    """
    pass


class HttpError(BitGoException):
    """ General Http error raised when interacting
        with BitGo's API"""
    pass


class BadRequest(HttpError):
    """HTTP 400: Bad Request"""
    pass


class Unauthorized(HttpError):
    """HTTP 401: Unauthorized"""
    pass


class Forbidden(HttpError):
    """HTTP 403: Forbidden"""
    pass


class NotFound(HttpError):
    """HTTP 404: Not Found"""
    pass


class NotAcceptable(HttpError):
    """HTTP 406: Not Acceptable"""
    pass

