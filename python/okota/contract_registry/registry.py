# standard imports
import os
import logging
import json
import hashlib

# third-party imports
from chainlib.eth.contract import (
        ABIContractEncoder,
        ABIContractType,
        abi_decode_single,
        )
from chainlib.chain import ChainSpec
from chainlib.eth.constant import (
        ZERO_ADDRESS,
        )
from chainlib.jsonrpc import JSONRPCRequest
from hexathon import (
        even,
        add_0x,
        )
from chainlib.eth.tx import TxFactory
from eth_contract_registry.registry import ContractRegistry
from eth_contract_registry.encoding import (
        to_identifier,
        from_identifier_hex,
        )
from eth_contract_registry import Registry

logg = logging.getLogger(__name__)

moddir = os.path.dirname(__file__)
datadir = os.path.join(moddir, '..', 'data')


class ContractRegistryAddressDeclarator(ContractRegistry):

    default_chain_spec = None
    __chains_registry = {}

    __abi = None
    __bytecode = None

    @staticmethod
    def abi():
        if ContractRegistryAddressDeclarator.__abi == None:
            f = open(os.path.join(datadir, 'RegistryAddressDeclarator.json'), 'r')
            ContractRegistryAddressDeclarator.__abi = json.load(f)
            f.close()
        return ContractRegistryAddressDeclarator.__abi


    @staticmethod
    def bytecode():
        if ContractRegistryAddressDeclarator.__bytecode == None:
            f = open(os.path.join(datadir, 'RegistryAddressDeclarator.bin'))
            ContractRegistryAddressDeclarator.__bytecode = f.read()
            f.close()
        return ContractRegistryAddressDeclarator.__bytecode


    @staticmethod
    def gas(code=None):
        return 3000000


    def constructor(self, sender_address, address_declarator, identifier_strings=[]):
        enc = ABIContractEncoder()
        enc.address(address_declarator)
        enc.uint256(64)
        enc.uint256(len(identifier_strings))
        for s in identifier_strings:
            enc.bytes32(to_identifier(s))
        data = enc.get_contents()

        tx = self.template(sender_address, None, use_nonce=True)
        tx = self.set_code(tx, ContractRegistryAddressDeclarator.bytecode() + data)
        logg.debug('bytecode {}\ndata {}\ntx {}'.format(ContractRegistryAddressDeclarator.bytecode(), data, tx))
        return self.build(tx)

