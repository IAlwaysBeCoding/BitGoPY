import json

from bitgo.client import BitGoClient
from bitgo.errors import (InvalidAccessToken,InvalidClient,
                          BitGoResourceException,InvalidResourceEndpoint,
                          InvalidResourceEndpointUrl,InvalidResourceMethod)

__all__ = ['BitGoResource','CreateMixin','ReadMixin',
           'ListMixin','UpdateMixin','DeleteMixin',
           'CRUDMixin']


class BitGoResource(object):

    """
        A base resource is a model representing an API resource from
        BitGo's API.Subclasses from this class usually offer several
        helper methods that makes talking to the RESTful API
        easy.This class is only meant to be used as a base class
        providing the bare requirements for interacting directly with
        the RESTful API. These requirements include an access token
        or a BitGoAccessToken instance, and a BitGoClient instance
        that is passed to every single new instance created from
        its subclass, and an ENDPOINT class variable.

        You can create a new instance by calling the request_resource()
        class method with an 'action', a BitGoClient instance, and
        an access_token.This calls the BitGo's API, parses the
        json data, and returns a new BitGoResource instance or subclass
        instance.The required 'action' points to a key in the ENDPOINT
        class variable which include a tuple that contains an endpoint url
        and a http method to call the resource.Any extra request data
        should be passed through the **kwargs dictionary, and any other
        url mappings should be passed through the *args tuple.


        It also is possible to instantiate BitGoResource objects
        from the json received from calling the RESTful API by using the
        'from_json()' class method,which serializes json into a new
        instance of this class or subclass.You can then use these
        resources to work behind the scenes with BitGO's API, or use
        these instances for simple data model objects.


        Note:ENDPOINT needs to be a dictionary for each unique
        resource's action(AKA:each http(s) call to BitGo's API).

        Each key inside ENDPOINT needs to include a 2 item tuple.
        The first item is the resource url, and the last is the
        type of http method to use for the request.The http method
        can be all lowercase or uppercase, it doesn't matter.



        Example:
            #Example of a custom endpoint for listing,adding
            #and getting a specific wallet.At the moment,you
            #can't currently delete wallets.
            ENDPOINT = {
                        'LIST':('wallet','GET'),
                        'ADD' :('wallet','POST'),
                        'GET' :('wallet/:id','GET')
                        }

        Make sure to remove the api version and anything before it.
        Correct:wallet
        Incorrect:/api/v1/wallet

    """
    ENDPOINT = None

    def __init__(self,client,access_token,properties={}):

        """
            Validates requirements and sets internal properties
            from the properties passed.

            @param client : A BitGoClient instance

            @param access_token : This can be a token represented in
                                a string or a BitGoAccessToken instance.

            @param properties : A dictionary representing the internal
                                properties for a BitGoResource.These
                                properties will be set to the current
                                instance via calling setattr().

        """
        #validate client and access_token
        self.validate_requirements(client=client,access_token=access_token)

        #sets the internal properties directly by adding to the internal
        #attritube dict to avoid triggering setattr
        self._client = client
        self._access_token = access_token

        self._properties = {}

        for key in properties:
            self._properties[key] = properties[key]

    def __getitem__(self,k):
        try:
            return self._properties[k]
        except KeyError:
            raise AttributeError

    def __getattr__(self,k):

        try:
            return getattr(self,k)
        except AttributeError:
            return self._properties[k]

    @classmethod
    def validate_access_token(cls,access_token):

        """
            Validates the access_token variable as being
            a str type or a valid instance of BitGoAccessToken,
            and anything else will raise an InvalidAccessToken.

        """

        if not isinstance(access_token,(str,BitGoAccessToken)):
            raise InvalidAccessToken('Not a valid BitGoAccessToken' \
                                     'instance or str was passed to access_token')

    @classmethod
    def validate_client(cls,client):

        """
            Validates to make sure client is an instance
            of BitGoClient or an instance from a sub class.

        """
        if not isinstance(client,BitGoClient):
            raise InvalidClient('Not a valid BitGoClient instance '\
                                'was passed to client')

    @classmethod
    def validate_requirements(cls,client,access_token):

        """
            Does a complete validation of the basic requirements
            which include a client and access token.Makes sure
            they both are right type of class.Otherwise,an
            InvalidClient or InvalidAccessToken might be raised.

        """
        cls.validate_client(client=client)
        cls.validate_access_token(access_token=access_token)

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self,value):
        #Raise an InvalidClient if value isn't an
        #instance of BitGoClient or a subclass.
        self._validate_client(client=client)
        self._client = value

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self,value):
        #Raise an InvalidAccessToken if value
        #isn't a valid access token that we can use
        self._validate_access_token(access_token=access_token)
        self._access_token = value

    @classmethod
    def endpoint(cls,action,*args):

        """ Returns the endpoint url to BitGo's API for the current
            resource class.All subclasses should specify a ENDPOINT
            representing the endpoint.

            @param *args:Args will be used for mapping to the ENDPOINT's url.
                         map_to_url() will replace args for any possible mutable
                         fragment.
        """

        def map_to_url(endpoint,*args):

            """
                Map additional arguments, to the resource's ENDPOINT.
                The ENDPOINT will be split by '/' into individual
                components. Every component will then be checked
                to see if it contains a colon":".If found, then the
                first item in args will be replaced with that component.
                Thus, giving a simple mechanism to map additional url
                fragments to the ENDPOINT.

                Note:Currently, if the number of args does not match
                the number of possible mappings, then an InvalidEndpoint
                will be raised.
            """

            fragments = endpoint.split('/')
            mutable_fragments = [f for f in fragments if f.startswith(':')]
            if len(args) != len(mutable_fragments):
                #Todo:Allow for args to contain more than the required arguments,
                #instead of raising an InvalidEndpoint exception.

                raise InvalidResourceEndpointUrl('Args does not match exact mutable ' \
                                                 'fragments.' \
                                                'ENDPOINT could not be mapped')

            args_list = list(args)

            has_mappings = lambda f,keys :keys.pop(0) if f.startswith(':') else f
            #Loop through all the url fragments and check to see if fragment starts with
            # a colon(:), if it does then replace the fragment by popping the first
            # key on the args_list.
            mapped_endpoint = "".join(['/{}'.format(has_mappings(f,args_list))
                                       for f in fragments])

            if mapped_endpoint.startswith('//'):
                return mapped_endpoint[1:len(mapped_endpoint)]
            else:
                return mapped_endpoint

        cls.check_endpoint_exists()
        endpoint,_ = cls.get_action_endpoint(action=action)
        return map_to_url(endpoint,*args)

    @classmethod
    def check_endpoint_exists(cls):
        """ Checks to make sure that there is an ENDPOINT '\
            class variable set and that it is atleast a
            dictionary variable.

        """
        klazz_endpoint_var = getattr(cls,'ENDPOINT',None)
        if klazz_endpoint_var is None:
            raise InvalidResourceEndpoint('Mixin missing the ENDPOINT ' \
                                          'class variable.Any class ' \
                                          'subclassing from this mixin ' \
                                          'must provide an ENDPOINT dictionary '\
                                          'whose keys provide a tuple for each '\
                                          'endpoint.The 2 item tuple must be '\
                                          'an endpoint url, and an http(s) method '\
                                          'for requesting the endpoint url.')

        if not isinstance(klazz_endpoint_var,dict):
            raise InvalidResourceEndpoint('Found the ENDPOINT class variable, but '\
                                          'it is not a valid dictionary')

    @classmethod
    def get_action_endpoint(cls,action):

        """
            Returns the endpoint tuple associated
            with a resource action.This tuple contains
            a url endpoint to the resource, and the http(s)
            method to use for requesting the resource.
            for the requested resource action.It verifies
            that a valid http(s) method is passed, and
            that the endpoint is a str type and nothing else.

        """

        endpoint,method = cls.ENDPOINT.get(action,None)
        if endpoint is None:
            raise InvalidResourceEndpoint('Cannot find resource method'\
                                        ' for resource action:{a}'.format(a=action))
        if not isinstance(endpoint,str):
            raise InvalidResourceEndpointUrl('Invalid resource endpoint url for'\
                                          ' resource action:{a}'.format(a=action))

        if method.upper() not in ['POST','GET','DELETE','PUT']:
            raise InvalidResourceMethod('HTTP method is invalid'\
                                        ' for resource action:{a}'.format(a=action))

        return endpoint,method

    @classmethod
    def request_resource(cls,action,client,access_token,return_json=False,*args,**kwargs):

        """
            Main method for requesting BitGo resources.This method
            checks to make sure there is an ENDPOINT class variable,
            then for a valid resource action, and last but not least
            that there is a valid http(s) method assigned to that
            specific endpoint.
            The only valids http(s) methods are:

                 * GET
                 * POST
                 * PUT
                 * DELETE

            @param action : The action name that links to a key inside
                            the ENDPOINT class. If no key is found an
                            InvalidResourceEndpoint is raised

            @param client : A BitGoClient instance

            @param access_token : An access token can be a str representing
                                  an access token or a BitGoAccessToken instance.

            @param return_json : If True, then it will use the json response
                                 data to create a new BitGoResource instance by
                                 calling from_json() method and passing the json
                                 data as an argument.


            @param *args: Extra arguments will mapped to the ENDPOINT by calling
                          map_to_url() inside the class method endpoint().

            @param **kwargs: Anything passed to kwargs
                             will be used as request data.

        """

        _, method =cls.get_action_endpoint(action=action)
        endpoint_mapped = cls.endpoint(action=action,*args)

        response = client.request(url=endpoint_mapped,
                                    method=method,
                                    params=kwargs,
                                    access_token=access_token)

        return cls.from_json(client=client,
                             access_token=access_token,
                             json_data=response,
                             action=action)

    @classmethod
    def from_json(cls,client,access_token,json_data,klazz_resource=None):

        """
            Helper function that takes a raw json string or
            a dictionary containing data to be used for building
            the properties of a new BitGoResource instance.It
            can also take a custom class that comforms to BitGoResource,
            API's.

            @param client : A BitGoClient instance

            @param access_token : This can be a token represented in
                                a string or a BitGoAccessToken instance.

            @param json_data :  A str or dict that will be the internal
                                properties for the new resource built.
                                These properties. If it is a str then
                                it needs to be a proper json string.

            @param klazz_resource : A compliant BitGoResource class or
                                    subclass for constructing an instance.
                                    If is set to None, then it will use a
                                    BitGoResource class as the default choice
                                    for constructing an instance.

        """
        if isinstance(json_data,str):
            try:
                json_data = json.loads(json_data)
            except ValueError:
                raise BitGoResourceException('Could not load json_data into json. ' \
                                            'Failed creating BitGoResource from json.')
        elif isinstance(json_data,dict):
            #If a class was passed to klazz_resource then use it
            if klazz_resource:
                #However,lets first check that it is a valid BitGoResource instance
                #or a subclassing instance
                if not isinstance(klazz_resource,BitGoResource):
                    raise BitGoResourceException('klazz_resource is not a valid instance '\
                                                 'of BitGoResource or a subclass of it')

                return klazz_resource(client=client,
                                      access_token=access_token,
                                      properties=json_data)
            else:
                return cls(client=client,
                           access_token=access_token,
                           properties=json_data)
        else:
            raise BitGoResourceException('Invalid json_data, it needs to be a str ' \
                                         ' or a dict in order to create a new BitGoResource')


class CreateMixin(object):

    """
        A generic mixin used for creating a new BitGoResource.
    """

    @classmethod
    def create(cls,client,access_token,*args,**kwargs):

        cls.validate_requirements(client=client,access_token=access_token)

        return cls.request_resource(action='CREATE',
                                    client=client,
                                    access_token=access_token,
                                    *args,
                                    **kwargs)


class ReadMixin(object):

    """
        A generic mixin used for getting a specific BitGoResource
        by id.
    """

    @classmethod
    def get(cls,client,access_token,resource_id,*args,**kwargs):

        cls.validate_requirements(client=client,access_token=access_token)

        #Creates a new list and add id to the end of the list
        #to avoid any problems building the url when calling
        #map_to_url().Thus,having the id of the resource at the
        #end of the url
        args = list(args).append(resource_id)
        return cls.request_resource(action='READ',
                                    client=client,
                                    access_token=access_token,
                                    *args,
                                    **kwargs)


class ListMixin(object):

    """
        A generic mixin used for listing all of the same
        BitGoResources.

    """

    @classmethod
    def list(cls,client,access_token,*args,**kwargs):

        cls.validate_requirements(client=client,access_token=access_token)

        return cls.request_resource(action='LIST',
                                    client=client,
                                    access_token=access_token,
                                    *args,
                                    **kwargs)


class UpdateMixin(object):

    """
        A generic mixin used for updating a BitGoResource by id.
    """

    @classmethod
    def update(cls,client,access_token,resource_id,*args,**kwargs):

        cls.validate_requirements(client=client,access_token=access_token)

        args = list(args).append(resource_id)
        return cls.request_resource(action='UPDATE',
                                    client=client,
                                    access_token=access_token,
                                    *args,
                                    **kwargs)


class DeleteMixin(object):

    """
        A generic mixin used for deleting a BitGoResource by id.
    """

    @classmethod
    def delete(cls,client,access_token,resource_id,*args,**kwargs):

        cls.validate_requirements(client=client,access_token=access_token)

        args = list(args).append(resource_id)
        return cls.request_resource(action='DELETE',
                                    client=client,
                                    access_token=access_token,
                                    *args,
                                    **kwargs)


class CRUDMixin(CreateMixin,ReadMixin,UpdateMixin,DeleteMixin):

    """
        A generic CRUD mixin, in other words this mixin can
        create,read,update and delete a BitGoResource.However,
        it cannot list multiple BitGoResource.
    """
    pass


if __name__ == '__main__':
    print 'yes'
