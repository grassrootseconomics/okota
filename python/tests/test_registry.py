# standard imports
import os
import unittest
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
from eth_address_declarator.unittest import TestAddressDeclaratorBase
from hexathon import add_0x

# local imports
from okota.contract_registry.registry import (
        ContractRegistryAddressDeclarator as ContractRegistry,
        to_identifier,
        )

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestContractRegistry(TestAddressDeclaratorBase):

    def setUp(self):
        super(TestContractRegistry, self).setUp()
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.rpc)
        c = ContractRegistry(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.constructor(self.accounts[0], self.address, ['FOO', 'BAR'])
        self.rpc.do(o)

        o = receipt(tx_hash_hex)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        self.registry_address = r['contract_address']


    def test_registry_declarator(self):
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.rpc)
        c = ContractRegistry(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)

        bogus_hash_two = bytearray(32)
        bogus_hash_two[0] = 0x01
        bogus_hash_two_hex = add_0x(bogus_hash_two.hex())
        (tx_hash_hex, o) = c.set(self.registry_address, self.accounts[0], 'FOO', self.registry_address)
        r = self.rpc.do(o)
        o = receipt(r)
        rcpt = self.rpc.do(o)
        self.assertEqual(rcpt['status'], 1)

        o = c.address_of(self.registry_address, 'FOO', sender_address=self.accounts[0])
        r = self.rpc.do(o)
        r = c.parse_address_of(r)
        self.assertEqual(r, strip_0x(self.registry_address))

        c = Declarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        o = c.declaration(self.address, self.accounts[0], self.registry_address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        proofs = c.parse_declaration(r)

        logg.debug('proofs {}'.format(proofs))
        s = to_identifier('FOO')
        h = hashlib.sha256()
        h.update(bytes.fromhex(strip_0x(s)))
        z = h.digest() 
        self.assertEqual(z.hex(), proofs[0])

        h = hashlib.sha256()
        h.update(str(self.chain_spec).encode('utf-8'))
        chain_description_hash = h.digest()
#
#        h = hashlib.sha256()
#        h.update(z)
#        h.update(chain_description_hash)
#        z = h.digest() 
#        self.assertEqual(z.hex(), proofs[1])
#
#        h = hashlib.sha256()
#        h.update(z)
#        h.update(bogus_hash_two)
#        z = h.digest() 
#        self.assertEqual(z.hex(), proofs[2])



if __name__ == '__main__':
    unittest.main()
