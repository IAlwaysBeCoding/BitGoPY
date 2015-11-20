
from bitgo.client import BitGoClient
from bitgo.errors import BitGoResourceException
from bitgo.resource import (BitGoResource,CRUDMixin,ListMixin)


__all__ = ['Wallets']


class Wallets(object):

    @classmethod
    def list(cls,params):
        pass

    @classmethod
    def add(cls,params):
        pass

    @classmethod
    def get(cls,params):
        pass

    @classmethod
    def remove(cls,params):
        pass

    @classmethod
    def get_wallet(cls,params):
        pass

    @classmethod
    def list_shares(cls,params):
        pass

    @classmethod
    def get_share(cls,params):
        pass

    @classmethod
    def update_share(cls,params):
        pass

    @classmethod
    def cancel_share(cls,params):
        pass

    @classmethod
    def accept_share(cls,params):
        pass

    @classmethod
    def create_key(cls,params):
        pass

    @classmethod
    def create_wallet_with_keychains(cls,params):
        pass

    @classmethod
    def create_forward_wallet(cls,params):
        pass

