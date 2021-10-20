pragma solidity >0.6.11;

// SPDX-License-Identifier: GPL-3.0-or-later


// TODO: inherit accounts index contract
contract AccountsIndexAddressDeclarator {

	address public tokenAddress;
	bytes32 tokenAddressHash;
	address public addressDeclaratorAddress;
	mapping(address => uint256) entryIndex;
	//uint256 count;
	mapping(address => bool) writers;
	address[] entries;

	address public owner;
	address newOwner;

	event AddressAdded(address indexed addedAccount, uint256 indexed accountIndex); // AccountsIndex
	event OwnershipTransferred(address indexed previousOwner, address indexed newOwner); // EIP173

	constructor(address _tokenAddress, address _addressDeclaratorAddress) public {
		bytes memory _tokenAddressPadded;
		owner = msg.sender;
		addressDeclaratorAddress = _addressDeclaratorAddress;
		tokenAddress = _tokenAddress;
		_tokenAddressPadded = abi.encode(tokenAddress);
		tokenAddressHash = sha256(_tokenAddressPadded);
		entries.push(address(0));
	}

	function add(address _account) external returns (bool) {
		bool ok;
		bytes memory r;
		uint256 oldEntryIndex;

		require(writers[msg.sender]);
		require(entryIndex[_account] == 0);

		(ok, r) = addressDeclaratorAddress.call(abi.encodeWithSignature("addDeclaration(address,bytes32)", _account, tokenAddressHash));
		require(ok);
		require(r[31] == 0x01);

		oldEntryIndex = entries.length - 1;
		entryIndex[_account] = oldEntryIndex;
		entries.push(_account);

		emit AddressAdded(_account, oldEntryIndex);
		return true;
	}

	// Implements AccountsIndex
	function have(address _account) external view returns (bool) {
		return entryIndex[_account] > 0;
	}

	// Implements AccountsIndex
	function entry(uint256 _idx) public returns (address) {
		return entries[_idx+1];
	}

	// Implements AccountsIndex
	function entryCount() public returns (uint256) {
		return entries.length - 1;
	}

	function addWriter(address _writer) public returns (bool) {
		require(owner == msg.sender);
		writers[_writer] = true;
		return true;
	}

	function deleteWriter(address _writer) public returns (bool) {
		require(owner == msg.sender);
		delete writers[_writer];
		return true;
	}

	// Implements EIP173
	function transferOwnership(address _newOwner) public returns (bool) {
		require(msg.sender == owner);
		newOwner = _newOwner;
		return true;
	}

	// Implements OwnedAccepter
	function acceptOwnership() public returns (bool) {
		address oldOwner;

		require(msg.sender == newOwner);
		oldOwner = owner; 
		owner = newOwner;
		newOwner = address(0);
		emit OwnershipTransferred(oldOwner, owner);
		return true;
	}
}
