#!/usr/bin/python3

import json
from pathlib import Path

import pytest
import solcx

import abi2solc

ABI_LIST = [json.load(i.open()) for i in Path(".").glob("tests/abi/*.json")]
SOLC_VERSIONS = ["0.4.17", "0.4.22", "0.4.25", "0.5.0", "0.5.10"]


@pytest.fixture(autouse=True)
def setup():
    for version in SOLC_VERSIONS:
        solcx.install_solc(version)


@pytest.mark.parametrize("abi", ABI_LIST)
@pytest.mark.parametrize("version", SOLC_VERSIONS)
def test_abi_solc5(abi, version):
    solcx.set_solc_version(version)
    interface = abi2solc.generate_interface(abi, "Test", version.startswith("0.4"))
    generated_abi = list(solcx.compile_source(interface).values())[0]["abi"]
    if next((i for i in abi if i["type"] == "constructor"), False):
        assert len(abi) == len(generated_abi) + 1
    else:
        assert len(abi) == len(generated_abi)
    for item in generated_abi:
        assert item in abi
