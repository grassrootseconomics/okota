# standard imports
import hashlib

# external imports
from chainlib.eth.constant import ZERO_ADDRESS

# local imports
from cic_contracts.accounts_index import CICAccountsIndex
from cic_contracts.registry import CICRegistry


class CICTokenIndex(CICRegistry, CICAccountsIndex):

    def address_of(self, contract_address, identifier_string, sender_address=ZERO_ADDRESS):
        h = hashlib.sha256()
        h.update(identifier_string.encode('utf-8'))
        z = h.digest()
        return super(CICTokenIndex, self).address_of_literal(contract_address, z.hex(), sender_address=sender_address)
