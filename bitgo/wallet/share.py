
from bitgo.client import BitGoClient
from bitgo.errors import BitGoResourceException
from bitgo.resource import (BitGoResource,CRUDMixin,ListMixin)

__all__ = ['BitGoWalletShare']


class BitGoWalletShare(BitGoResource,CRUDMixin,ListMixin):

    """
        A BitGoWalletShare provides with all of the necessary
        methods to implement the BitGo's wallet sharing API.
        This includes at the moment 5 BitGo wallet
        operations:

            * Sharing a wallet
            * List Wallet Shares
            * Accept Wallet Share(A client operation)
            * Cancel Wallet Share
            * Remove Wallet Share
              from a User

        Only 1 of the 5 BitGo's wallet operations is a client
        side operation. This means that nothing will be sent
        back to the server and everything will be performed
        without having to call any endpoint. Thus, the operation
        will not require an access token.

        Most of BitGoWalletShare's methods will require a
        walletid associated with the wallet where the wallet
        sharing is happening.

        This resource will try to comform to the original wallet
        share's API from BitGoJS. It implements the same methods
        that are found inside wallet.js and wallets.js that relate
        to wallet shares. In other words, it will try to resemble
        the original API by implementing the same public methods,
        but in snake case instead of camel case.


    """

        ENDPOINT = {'CREATE':,
                    'READ':,
                    'UPDATE':,
                    'DELETE':,
                    'LIST':,
    @classmethod
    def share_wallet(cls,email,permissions,wallet_password,skip_keychain,disable_email):

        """
            This operation shares a wallet to anyone via email.A
            unique set of wallet permissions can be given to any
            user, with or without a pass phrase(password). This
            essentially shares the private key with the an authorized
            user. The owner and the authorized user of the wallet
            create a set of public-private keypairs during the signup
            process.

            Basically, this class method returns a new instance of
            BitGoWalletShare after successfully calling BitGo's API
            and creating a wallet share on their servers.

            Documentation from BitGo summarizes what eventually
            happens during a wallet share.

            https://www.bitgo.com/api/#sharing-a-wallet

            * Get the receiving user's sharing
              key (a derived path of the receiver's public key)

            * Decrypt the wallet to be shared locally.

            * Re-encrypt the wallet against the public key above, so
              that only the receiver may decrypt it.

            * Upload the encrypted keys to the BitGo service, which
              informs the receiver they have a pending share.


            This method comforms to Wallet.shareWallet() and it is
            the same name method but in snake cased.

            @param email : A str representing an email of the user to share
                           the wallet with.

            @param permissions : A list or tuple of str representing the
                                 permissions that the wallet share entails
                                 to the authorized user. These permissions
                                 include :

                                    * View - View transactions on the wallet

                                    * Spend - Initiate transactions on the
                                              wallet, which are subject to
                                              wallet policy

                                    * Admin - Change policy and manage users and
                                              settings on the wallet

            @wallet_password : A str representing a password on the wallet being
                               shared to the authorized user.

            @skip_keychain : A boolean which can be set to True if the authorized
                             user will be using the keychain out-of-band

            @disable_email : Set to True to prevent a notification email being sent
                             to the newly added authorized user.

        """

    @classmethod
    def list_shares(cls,client,access_token,retrieve=True):

        """
            Gets a list of incoming and outgoing wallet shares for the
            logged-on account.

            This method comforms to Wallets.listShares() and it is
            the same name method but in snake cased.

            @param client: A BitGoClient instance

            @param access_token : An access token can be a str representing
                                an access token or a BitGoAccessToken instance.

            @param retrieve : Boolean deciding whether to retrieve each
                              wallet share from the retrieved meta data.
                              If False, then a list of individual dictionaries
                              with each containing either an incoming or outgoing
                              wallet share data on the current logged-on account.

        """

        client.request_resource(action='LIST',
                                client=client,
                                access_token=access_token,

 
    def accept_share(self):

        """
            This operation requires the session to be unlocked using the Unlock API.
            Client-side operation to accept a wallet share. Performs the following steps:

            This method performsGet the incoming wallet share, including the encrypted private keychain.
                Using the user's sharing private key and the wallet share xPub, derive the key to decrypt the private keychain.
                Re-encrypt the wallet with the user's chosen passphrase for future use.
                Upload the encrypted keys to the BitGo service and sets the share to accepted, giving the user access to the wallet on BitGo.
        """

