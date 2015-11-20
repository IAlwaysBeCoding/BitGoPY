
from bitgo.client import BitGoClient
from bitgo.errors import BitGoResourceException
from bitgo.resource import (BitGoresource,CreateMixin,
                            ReadMixn,UpdateMixin,ListMixin)

__all__ = ['BitGoKeychains']


class BitGoKeychains(BitGoResource,
                     CreateMixin,
                     ReadMixin,
                     UpdateMixin,
                     ListMixin):


    def is_valid(self,params):
        pass

    @classmethod
    def list(cls,client,access_token,skip=0,limit=100):
        super(BitGoKeyChains,cls).list()

    def create(self,params):
        pass

    def add(self,params):
        pass

    def create_bitgo(self,params):
        pass

    def create_backup(self,params):
        pass

    def get(self,params):
        pass

    def update(self,params):
        pass


