# Okota

Okota implements smart contract registries for the CIC network with the Address Declarator backend.

For every entry added to the registry, a declaration is added aswell.


## Contract declaration translations

| registry call | declarator | subject | proof |
|---|---|---|---|
| ContractRegistry.set(registry\_identifier, contract\_address) | sender | contract\_address | registry\_identifier |
| AccountsIndex.register(wallet\_address) | sender | wallet\_address | token address of accounts index |
| TokenRegistry.registry(token\_address) | sender | token\_address | sha256(token symbol) |


## Query the declarator with CLI

`eth-accounts-index-view -e <declarator_contract> -a <declarator_address> <subject_address>`


## Add arbitrary other proofs with CLI

`eth-accounts-index-add -e <declarator_contract> -y <keyfile_of_declarator> -a <subject_address> <256 bit proof in hex>`
