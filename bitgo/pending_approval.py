from bitgo.client import BitGoClient
from bitgo.errors import BitGoResourceException
from bitgo.resource import (BitGoResource,CRUDMixin,ListMixin)


__all__ = ['BitGoPendingApprovals']

class BitGoPendingApprovals(BitGoResource,CRUDMixin,ListMixin):

    def id(self):
        pass

    def owner_type(self,params):
        pass

    def wallet_id(self):
        pass

    def enterprise_id(self):
        pass

    def state(self):
        pass

    def creator(self):
        pass

    def type(self):
        pass

    def info(self):
        pass

    def url(self):
        pass

    def get(self,params):
        pass

    def populate_wallet(self):
        pass

    def recreate_and_sign_transaction(self,params):
        pass

    def construct_approval_tx(self,params):
        pass

    def approve(self,params):
        pass

    def reject(self,params):
        pass

    def cancel(self,params):
        pass



