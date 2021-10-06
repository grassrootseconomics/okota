# standard imports
import os
import unittest
import logging

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

        bogus_hash_one = add_0x(os.urandom(32).hex())
        bogus_hash_two = add_0x(os.urandom(32).hex())
        (tx_hash_hex, o) = c.set(self.registry_address, self.accounts[0], 'FOO', self.registry_address, bogus_hash_one, bogus_hash_two)
        r = self.rpc.do(o)
        o = receipt(r)
        rcpt = self.rpc.do(o)
        assert rcpt['status'] == 1


if __name__ == '__main__':
    unittest.main()
