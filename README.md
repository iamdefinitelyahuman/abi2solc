# abi2solc

[![Pypi Status](https://img.shields.io/pypi/v/abi2solc.svg)](https://pypi.org/project/abi2solc/) [![Build Status](https://img.shields.io/travis/com/iamdefinitelyahuman/abi2solc.svg)](https://travis-ci.com/iamdefinitelyahuman/abi2solc) [![Coverage Status](https://coveralls.io/repos/github/iamdefinitelyahuman/abi2solc/badge.svg?branch=master)](https://coveralls.io/github/iamdefinitelyahuman/abi2solc?branch=master)

A library for generating Solidity interfaces from ABIs.

## Installation

You can install the latest release via ``pip``:

```bash
$ pip install abi2solc
```

Or clone the repo and use ``setuptools`` for the most up-to-date version:

```bash
$ python setup.py install
```

## Usage

```python
>>> import abi2solc

>>> abi = [{'constant': False, 'inputs': [{'name': 'spender', 'type': 'address'}, ...
>>> interface = abi2solc.generate_interface(abi, "TestInterface")

>>> print(interface)
'''pragma solidity ^0.5.0;

interface ExampleInterface {
     event Approval (address indexed tokenOwner, address indexed spender, uint256 tokens);
     event Transfer (address indexed from, address indexed to, uint256 tokens);

     function approve (address spender, uint256 tokens) external returns (bool success);
     function transfer (address to, uint256 tokens) external returns (bool success);
     function transferFrom (address from, address to, uint256 tokens) external returns (bool success);
     function allowance (address tokenOwner, address spender) external view returns (uint256 remaining);
     function balanceOf (address tokenOwner) external view returns (uint256 balance);
     function totalSupply () external view returns (uint256);
}'''
```

## Supported Versions

* By default, `abi2solc` generates interfaces with pragma `^0.5.0`
* With the `solc4=True` kwarg, interfaces are generated with pragma `^0.4.17`
* If `solc4=True` and the ABI also contains tuple types, an [abstract base contract](https://solidity.readthedocs.io/en/v0.4.25/contracts.html#abstract-contracts) is generated with pragma `^0.4.22`

## Tests

To run the test suite:

```bash
$ tox
```

Tests make use of [``py-solc-x``](https://github.com/iamdefinitelyahuman/py-solc-x).

## Development

This project is still under active development and should be considered a beta. Comments, questions, criticisms and pull requests are welcomed! Feel free to open an issue if you encounter a problem or would like to suggest a new feature.

## License

This project is licensed under the [MIT license](LICENSE).
