# standard imports
import unittest
import logging
import hashlib

# external imports
from eth_accounts_index import AccountsIndex
from chainlib.eth.nonce import RPCNonceOracle
from giftable_erc20_token import GiftableToken
from chainlib.eth.tx import receipt
from chainlib.eth.contract import ABIContractEncoder
from eth_address_declarator import Declarator
from eth_address_declarator.unittest import TestAddressDeclaratorBase

# local imports
from okota.accounts_index import AccountsIndexAddressDeclarator
from eth_accounts_index.registry import AccountRegistry

# test imports

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestAccountsIndex(TestAddressDeclaratorBase):

    def setUp(self):
        super(TestAccountsIndex, self).setUp()
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.rpc)

        c = AccountsIndexAddressDeclarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.constructor(self.accounts[0], self.foo_token_address, self.address)
        r = self.rpc.do(o)

        o = receipt(tx_hash_hex)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        self.accounts_index_address = r['contract_address']
        logg.debug('accounts index deployed with address {}'.format(self.accounts_index_address))

        c = AccountRegistry(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.add_writer(self.accounts_index_address, self.accounts[0], self.accounts[0])
        r = self.rpc.do(o)

        o = receipt(tx_hash_hex)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)


    def test_accounts_index_address_declarator(self):
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.rpc)
        c = AccountsIndex(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.add(self.accounts_index_address, self.accounts[0], self.accounts[1])
        r = self.rpc.do(o)
        self.assertEqual(tx_hash, r)

        self.helper.mine_block()

        o = receipt(tx_hash)
        rcpt = self.rpc.do(o)
        self.assertEqual(rcpt['status'], 1)
        for k in rcpt.keys():
            logg.debug('>>> RCPT {}??{}'.format(k, rcpt[k]))

        o = c.have(self.accounts_index_address, self.accounts[1], sender_address=self.accounts[0])
        r = self.rpc.do(o)

        c = Declarator(self.chain_spec) #, signer=self.signer, nonce_oracle=nonce_oracle)
        o = c.declaration(self.address, self.accounts[0], self.accounts[1], sender_address=self.accounts[0])
        r = self.rpc.do(o)
        proofs = c.parse_declaration(r)

        enc = ABIContractEncoder()
        enc.address(self.foo_token_address)
        token_address_padded = enc.get()
        logg.debug('proof??{} {}'.format(proofs, token_address_padded))
        h = hashlib.sha256()
        h.update(bytes.fromhex(token_address_padded))
        r = h.digest()
        self.assertEqual(r.hex(), proofs[0])


if __name__ == '__main__':
    unittest.main()
