# standard imports
import os
import unittest
import json
import logging
import hashlib

# external imports
from chainlib.eth.unittest.ethtester import EthTesterCase
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.tx import receipt
from giftable_erc20_token import GiftableToken
from chainlib.eth.tx import unpack
from hexathon import strip_0x
from chainlib.eth.contract import ABIContractEncoder
from eth_address_declarator import Declarator

# local imports
from okota.token_index.index import (
        TokenUniqueSymbolIndexAddressDeclarator as TokenIndex,
        CICTokenIndex,
        to_identifier,
        )

# test imports
from eth_address_declarator.unittest import TestAddressDeclaratorBase

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

testdir = os.path.dirname(__file__)


class TestTokenIndex(TestAddressDeclaratorBase):

    def setUp(self):
        super(TestTokenIndex, self).setUp()
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.rpc)
        c = TokenIndex(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.constructor(self.accounts[0], self.address)
        self.rpc.do(o)

        o = receipt(tx_hash_hex)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        self.token_index_address = r['contract_address']

        c = CICTokenIndex(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.add_writer(self.token_index_address, self.accounts[0], self.accounts[0])
        r = self.rpc.do(o)

        o = receipt(tx_hash_hex)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)



    def test_register(self):
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.rpc)
        c = CICTokenIndex(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        
        (tx_hash_hex, o) = c.add(self.token_index_address, self.accounts[0], self.foo_token_address)
        self.rpc.do(o)
        e = unpack(bytes.fromhex(strip_0x(o['params'][0])), self.chain_spec)

        o = receipt(tx_hash_hex)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        o = c.address_of(self.token_index_address, 'FOO', sender_address=self.accounts[0])
        r = self.rpc.do(o)
        address = c.parse_address_of(r)
        self.assertEqual(address, strip_0x(self.foo_token_address))
        
        o = c.entry(self.token_index_address, 0, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        address = c.parse_entry(r)
        self.assertEqual(address, strip_0x(self.foo_token_address))
        
        o = c.entry_count(self.token_index_address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        count = c.parse_entry_count(r)
        self.assertEqual(count, 1)
    
        c = Declarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        o = c.declaration(self.address, self.accounts[0], self.foo_token_address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        proofs = c.parse_declaration(r)
    
        h = hashlib.sha256()
        h.update('FOO'.encode('utf-8'))
        z = h.digest()

        self.assertEqual(proofs[0], z.hex())


if __name__ == '__main__':
    unittest.main()
