# Okota

Okota implements smart contract registries for the CIC network with the [Address Declarator](https://gitlab.com/cicnet/eth-address-index)  backend.

For every entry added to the registry, a declaration is added aswell.


## Contract declaration translations

| registry call | declarator | subject | proof |
|---|---|---|---|
| ContractRegistry.set(registry\_identifier, contract\_address) | sender | contract\_address | registry\_identifier |
| AccountsIndex.register(wallet\_address) | sender | wallet\_address | token address of accounts index |
| TokenRegistry.registry(token\_address) | sender | token\_address | sha256(token symbol) |


## Using the CLI

In the below, all in hex:

* `contract_address` is the address of the deployed Address Declarator contract.
* `subject_address` is the address a declaration is being made about.
* `declarer` is the entity making a declaration about the `subject_address`.
* `proof` a 256-bit proof

## Query the declarator with CLI

`eth-accounts-index-view -e <contract_address> -a <declarer_address> <subject_address>`


## Add arbitrary other proofs with CLI

`eth-accounts-index-add -e <contract_address> -y <declarer_keyfile> -a <subject_address> <proof>`
