
from bitgo.client import BitGoClient
from bitgo.errors import BitGoResourceException
from bitgo.resource import (BitGoResource,CRUDMixin,ListMixin)


class BitGoWallet(BitGoResource,CRUDMixin,ListMixin):

    def id(self):
        pass

    def label(self):
        pass

    def balance(self):
        pass

    def confirmed_balance(self):
        pass

    def unconfirmed_sends(self):
        pass

    def unconfirmed_receives(self):
        pass

    def type(self):
        pass

    def url(self,extra):
        pass

    def pending_approvals(self):
        pass

