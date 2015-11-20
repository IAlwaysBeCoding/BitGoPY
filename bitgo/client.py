import json
import requests

from bitgo.errors import (BitGoException,BitGoClientException,
                          InvalidAccessToken,HttpError,
                          BadRequest,Unauthorized,Forbidden,
                          NotFound,NotAcceptable)
from bitgo.token import BitGoAccessToken
from bitgo.version import VERSION

__all__ = ['BitGoClient']

class BitGoClient(object):

    """ BitGo's RESTful API client for requesting resources.

        Currently 2 endpoint environments are supported:
            test = 'https://test.bitgo.com/api/v1'
            prod = 'https://bitgo.com/api/v1'

    """

    USER_AGENT = 'BitGoPY PythonClient v{version}'.format(version=VERSION)
    ENVIRONMENT = {'test':'https://test.bitgo.com/api/v1',
                   'prod':'https://bitgo.com/api/v1'}

    def __init__(self,env=None,user_agent=None,proxy=None):

        """ Default environment will be set to 'test', if you want to use
            a different environment, you can pass a new supported environment
            string to parameter 'env'.

            @param env : environment string that will set the endpoint to use.
                        'test' or 'prod' are the only 2 acceptable endpoints
                        at this time.

            @param user_agent : User-Agent to use for every request sent.
                                Defaults to using the class default.

            @param proxy : Proxy to use when interacting through
                            BitGo's API.If passed, proxy needs to
                            be a dict with 2 keys(ip,port) minimum
                            and 4 maximum keys. The keys are:
                                'ip' = The IP of the proxy
                                'port' = The port of the proxy
                                'username' = optional username
                                'password' = optional password

                            Note: Only pass a username and password if
                            the proxy requires authentication, otherwise
                            leave a None value or don't passed a key
                            containing 'username' and 'password'

                            It is important to remember that access tokens
                            are bound to 1 ip.
        """

        self.endpoint = env or self.ENVIRONMENT['test']
        self.user_agent = user_agent or self.USER_AGENT

        if proxy:
            #Validate proxy before assigning it
            self._validate_proxy(proxy=proxy)

        self.proxy = proxy

    def _validate_proxy(self,proxy):

        """ Validates a proxy to make sure is either None value or a dictionary
            containing atleast 2 keys: 'ip' and 'port' keys, and/or 'username'
            and 'password' keys if proxy authentication is required
        """

        if proxy is not None:
            if not isinstance(proxy,dict):
                    raise BitGoClientException('Invalid proxy settings. Please '\
                                         'include a dictionary with "ip" and "port" '\
                                         'keys minimum, else leave it as None')

            if not all(key in proxy.keys() for key in ('ip','port','username','password')):
                #If ip and port are not the sole keys then raise an BitGoException
                if not all(key in proxy.keys() for key in ('ip','port')):
                    raise BitGoClientException('Missing ip or port key in proxy dict')

    def _build_proxy(self,proxy):

        """
            This function builds a correct proxy dictionary using the proxy provided.
            The requests library requires a proxy to be passed in a dictionary a
            certain way, so this function takes care of building that dictionary
            out of the given proxy.If proxy is None, then it returns None.
        """

        if proxy:
            #check whether username or password exists.if it exists include it on the proxy string
            if ('username' not in proxy) or ('password' not in proxy):
                proxy_string = 'http://{ip}:{port}'.format(ip=proxy['ip'],port=proxy['port'])
            else:
                proxy_string = 'http://{username}:{password}@{ip}:{port}'.format(username=proxy['username'],
                                                                                password=proxy['password'],
                                                                                ip=proxy['ip'],
                                                                                port=proxy['port'])

            #return the newly built proxy settings
            return {'http':proxy_string,
                    'https':proxy_string}

    def set_proxy(self,proxy):

        """ Function used to change proxy when needed. Make sure to passed
            a valid dictionary containing the right proxy configuration keys.
            Atleast, an 'ip' and 'port' key should be supplied
        """

        #Validate the proxy and make sure it is the correct format
        self._validate_proxy(proxy=proxy)
        #set proxy
        self.proxy = proxy

    def _build_url(self,uri):

        """ Builds the complete url by combining the endpoint and uri
        """
        if uri.startswith('/'):
            return '{endpoint}{resource}'.format(endpoint=self.endpoint,
                                                resource=uri)
        else:
            return '{endpoint}/{resource}'.format(endpoint=self.endpoint,
                                                  resource=uri)

    def _send_request(self,resource,method='get',params=None,access_token=None):

        """
            Internal private method for internal use only.
            All params will be converted to json before sending,
            and headers will be updated with a 'Content-Type: application/json'
            on every request, as well as with an access token if provided

       """

        http_method = {'get':requests.get,
                       'post':requests.post,
                       'put':requests.put,
                       'delete':requests.delete}

        #lookup http method to use
        request = http_method.get(method.lower(),None)

        #Makes sure a valid method was passed. If not raise a BitGoException.
        if request is None:
            raise BitGoClientException('Invalid http method,only acceptable methods' \
                                 ' are GET,POST,PUT, or DELETE')

        #Setup access token by seeing if access_token is a BitGoAccessToken
        #instance. If it is not check if access_token is a string else raise
        # InvalidAccessToken exception.
        if access_token:
            if isinstance(access_token,BitGoAccessToken):
                token = access_token.token
            elif isinstance(access_token,str):
                token = access_token
            else:
                raise InvalidAccessToken('access_token is not a valid str' \
                                         ' or a BitGoAccessToken instance')
        else:
            token = None

        #Sets http headers with User-Agent and Content-Type
        headers = {'Content-type':'application/json',
                   'User-Agent':self.user_agent}

        #If a token was provided , then update token in headers.
        if token:
            headers.update({'Authorization': 'Bearer {token}'.format(token=token)})

        #build the url
        url = self._build_url(uri=resource)
        print 'full url:{}'.format(url)
        #build the proxy configurations
        proxy = self.proxy if self.proxy is None else self._build_proxy(proxy=self.proxy)

        if method.lower() in ['delete','get']:
            return request(url,headers=headers,proxies=proxy)
        else:
            #If there are any params then convert it to json
            if params and isinstance(params,dict):
                json_data = json.dumps(params)
            else:
                json_data = None

            return request(url,data=json_data,headers=headers,proxies=proxy)

    def request(self,url,method='get',params=None,access_token=None):

        """ Sends a request to BitGo's API and handles any http errors
            that might occur.

            It can also send requests with an access token in the headers if
            given one .An access token can be provided with either a string
            representing the access token or a BitGoAccessToken object.

            Note:You must provide an access token for any request that requires
            authentication else the request will raise an Unauthorized exception.

            *Tokens are valid for 60 minutes, after expiration the user must re-authenticate.
            *Tokens are bound to a single IP address.

            @param url : resource's url that will be used to build the full
                              url combined with the client's endpoint.

            @param method : Http method to use. Valid options are 'get','post',
                            'put' or 'delete'.

            @param params : A dictionary object containing params to send. The
                            params will be converted to json before being sent

            @param access_token : An access token can be provided with a string or
                                an instance of a BitGoAccessToken object.

        """
        try:
            response = self._send_request(resource=url,
                                          method=method,
                                          params=params,
                                          access_token=access_token)
            #Lets make sure to raise a requests exception for
            #any client error or server error response.
            #This means any 4xx(client) or 5xx(server) http status code.
            #For everything else reraise a general BitGoException, except
            # for invalid access token error.
            response.raise_for_status()

        except requests.exceptions.ProxyError:
            raise BitGoException('A proxy error has occured while using  '\
                                 'the current proxy')

        except requests.exceptions.SSLError:
            raise BitGoException('A SSL error has occured')

        except requests.exceptions.ConnectionError:
            raise BitGoException("A http connection error has occured while connecting "\
                                 " to BitGo's. This is not a SSL or proxy error")

        except requests.exceptions.Timeout:
            raise BitGoException("A http timeout error has occured while connecting " \
                                 " to BitGo's.")

        except requests.exceptions.HTTPError:
            #Map for 4xx errors to a specific
            # BitGo's HttpError exception
            http_exceptions = {400:BadRequest,
                               401:Unauthorized,
                               403:Forbidden,
                               404:NotFound,
                               406:NotAcceptable}

            http_code = response.status_code
            #Check if we have here a client error status code,
            #AKA 4xx error
            is_client_error = http_exceptions.get(http_code,False)

            if is_client_error:
                client_exception = http_exceptions.get(http_code)
                error = '' if 'error' not in response.json() else response.json()['error']

                raise client_exception("BitGo API call failed.Response returned a "\
                                       "{code} http status code with "\
                                       "error: {error}".format(code=http_code,error=error))
            else:
                #Unknown http status code was returned. Something is very wrong.
                #Raise a general BitgoException addressing this anomaly.
                raise HttpError('BitGo returned a {code} http status. '\
                                     'This is definitely an anomaly'.format(code=http_code))

        except requests.exceptions.RequestException as exc:
            #Re-raise any other requests exception as a BitGoException
            raise BitGoException('An unknown requests exception has occured:{exc}'.format(exc))

        else:
           return response.json()

    def get(self,url,access_token=None):

        """ Sends a GET request with or without an access token"""

        return self.request(url=url,
                            method='get',
                            access_token=access_token)

    def delete(self,url,access_token=None):

        """ Sends a DELETE request with or without an access token"""

        return self.request(url=url,
                            method='delete',
                            access_token=access_token)


    def post(self,url,data,access_token=None):

        """ Sends a POST request with post's data and
            with or without an access token"""

        return self.request(url=url,
                            method='post',
                            params=data,
                            access_token=access_token)

    def put(self,url,data,access_token=None):

        """ Sends a PUT request with put's data and
            with or without an access token"""

        return self.request(url=url,
                            method='put',
                            params=data,
                            access_token=access_token)
'''
    def encrypt(self,password,input):

        if (password and input):
            sjcl.decry
'''
if __name__ == '__main__':
    from bitgo import BitGoClient
    print bin(BitGoClient())

