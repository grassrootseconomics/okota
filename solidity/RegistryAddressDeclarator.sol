pragma solidity >0.6.11;

// Author:	Louis Holbrook <dev@holbrook.no> 0826EDA1702D1E87C6E2875121D2E7BB88C2A746
// SPDX-License-Identifier:	GPL-3.0-or-later
// File-version: 2
// Description: Top-level smart contract registry for the CIC network


contract ContractRegistryAddressDeclarator {
	// Implements EIP 173
	address public owner;
	address public addressDeclarator;

	bytes32[] public identifiers;
	mapping (bytes32 => address) entries;		// contractidentifier -> address
	mapping (bytes32 => bytes32) chainIdentifiers;	// contractidentifier -> chainidentifier
	mapping (bytes32 => bytes32) chainConfigs; 	// chainidentifier -> chainconfig

	constructor(address _addressDeclarator, bytes32[] memory _identifiers) public {
		owner = msg.sender;
		for (uint i = 0; i < _identifiers.length; i++) {
			identifiers.push(_identifiers[i]);
		}
		addressDeclarator = _addressDeclarator;
	}

	function set(bytes32 _identifier, address _address, bytes32 _chainDescriptor, bytes32 _chainConfig) public returns (bool) {
		require(msg.sender == owner);
		require(entries[_identifier] == address(0));

		bool ok;
		bytes memory r;
		bool found = false;
		bytes32 identifierHash;
		bytes memory buf;
		uint8 i;

		for (i = 0; i < identifiers.length; i++) {
			if (identifiers[i] == _identifier) {
				found = true;
			}	
		}
		require(found, 'ERR_IDENTIFIER');

		buf = new bytes(32);
		for (i = 0; i < 32; i++) {
			buf[i] = _identifier[i];
		}
		identifierHash = sha256(buf);
		(ok, r) = addressDeclarator.call(abi.encodeWithSignature("addDeclaration(address,bytes32)", _address, identifierHash));
		require(ok);
		require(r[31] == 0x01);

		buf = new bytes(64);
		for (i = 0; i < 32; i++) {
			buf[i] = identifierHash[i];
		}
		for (i = 0; i < 32; i++) {
			buf[i+32] = _chainDescriptor[i];
		}

		identifierHash = sha256(buf);
		(ok, r) = addressDeclarator.call(abi.encodeWithSignature("addDeclaration(address,bytes32)", _address, identifierHash));
		require(ok);
		require(r[31] == 0x01);


		for (i = 0; i < 32; i++) {
			buf[i] = identifierHash[i];
		}
		for (i = 0; i < 32; i++) {
			buf[i+32] = _chainConfig[i];
		}
		identifierHash = sha256(buf);
		(ok, r) = addressDeclarator.call(abi.encodeWithSignature("addDeclaration(address,bytes32)", _address, identifierHash));
		require(ok);
		require(r[31] == 0x01);

		entries[_identifier] = _address;
		chainIdentifiers[_identifier] = _chainDescriptor;
		chainConfigs[_chainDescriptor] = _chainConfig;

		return true;
	}

	// Implements EIP 173
	function transferOwnership(address _newOwner) public returns (bool) {
		require(msg.sender == owner);
		owner = _newOwner;
		return true;
	}

	// Implements Registry
	function addressOf(bytes32 _identifier) public view returns (address) {
		return entries[_identifier];
	}

	function chainOf(bytes32 _identifier) public view returns (bytes32) {
		return chainIdentifiers[_identifier];
	}

	function configSumOf(bytes32 _chain) public view returns (bytes32) {
		return chainConfigs[_chain];
	}

	// Implements EIP 165
	function supportsInterface(bytes4 _sum) public pure returns (bool) {
		if (_sum == 0xbb34534c) { // Registry
			return true;
		}
		if (_sum == 0x01ffc9a7) { // EIP165
			return true;
		}
		if (_sum == 0x9493f8b2) { // EIP173
			return true;
		}
		return false;
	}
}
