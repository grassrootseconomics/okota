SOLC = /usr/bin/solc

all: token_index accounts_index contract_registry

token_index:
	$(SOLC) TokenUniqueSymbolIndexAddressDeclarator.sol --abi --evm-version byzantium | awk 'NR>3' > TokenUniqueSymbolIndexAddressDeclarator.json
	$(SOLC) TokenUniqueSymbolIndexAddressDeclarator.sol --bin --evm-version byzantium | awk 'NR>3' > TokenUniqueSymbolIndexAddressDeclarator.bin
	truncate -s -1 TokenUniqueSymbolIndexAddressDeclarator.bin


accounts_index:
	$(SOLC) AccountsIndexAddressDeclarator.sol --abi --evm-version byzantium | awk 'NR>3' > AccountsIndexAddressDeclarator.json
	$(SOLC) AccountsIndexAddressDeclarator.sol --bin --evm-version byzantium | awk 'NR>3' > AccountsIndexAddressDeclarator.bin
	truncate -s -1 AccountsIndexAddressDeclarator.bin

contract_registry:
	$(SOLC) RegistryAddressDeclarator.sol --abi --evm-version byzantium | awk 'NR>3' > RegistryAddressDeclarator.json
	$(SOLC) RegistryAddressDeclarator.sol --bin --evm-version byzantium | awk 'NR>3' > RegistryAddressDeclarator.bin
	truncate -s -1 RegistryAddressDeclarator.bin


install: all
	cp -v TokenUniqueSymbolIndexAddressDeclarator.{json,bin} ../python/okota/data/
	cp -v AccountsIndexAddressDeclarator.{json,bin} ../python/okota/data/
	cp -v RegistryAddressDeclarator.{json,bin} ../python/okota/data/
	
.PHONY: test install
