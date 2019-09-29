#!/usr/bin/python3

from copy import deepcopy
from typing import Dict, List


def _get_struct_map(abi_params: List[Dict], struct_map: Dict) -> None:
    struct_abi = [i for i in abi_params if "components" in i]

    for item in struct_abi:
        if [i for i in item["components"] if "components" in i]:
            _get_struct_map(item["components"], struct_map)
        s = tuple((i["name"], i["type"]) for i in item["components"])
        key = next((k for k, v in struct_map.items() if v == s), None)
        if not key:
            key = f"Tuple{len(struct_map)+1}"
            struct_map[key] = s
        item["type"] = item["type"].replace("tuple", key)


def generate_structs(abi: List[Dict]) -> List:
    structs: Dict = {}

    for item in abi:
        abi_params = item.get("inputs", []) + item.get("outputs", [])
        _get_struct_map(abi_params, structs)

    result = []
    for key, value in structs.items():
        value = " ".join(f"{i[1]} {i[0]};" for i in value)
        result.append(f"struct {key} {{ {value} }}")

    return result


def _format_param(param: Dict) -> str:
    formatted = param["type"]
    if param.get("indexed"):
        formatted += " indexed"
    if param.get("name"):
        formatted += f" {param['name']}"
    return formatted


def _format_params(abi_params: List[Dict]) -> str:
    return f"({', '.join(_format_param(i) for i in abi_params)})"


def generate_events(abi: List[Dict]) -> List:
    events_abi = sorted([i for i in abi if i["type"] == "event"], key=lambda k: k["name"])

    result = []
    for event in events_abi:
        result.append(f"event {event['name']} {_format_params(event['inputs'])};")

    return result


def generate_functions(abi: List[Dict]) -> List:
    fn_abi = sorted(
        [i for i in abi if i["type"] == "function"],
        key=lambda k: (k["stateMutability"], k.get("name", "")),
    ) + next(([i] for i in abi if i["type"] == "fallback"), [])

    result = []
    for fn in fn_abi:
        fn_str = "function "
        if fn.get("name"):
            fn_str += f"{fn['name']} "
        fn_str += _format_params(fn.get("inputs", []))
        fn_str += " external"
        if fn["stateMutability"] != "nonpayable":
            fn_str += f" {fn['stateMutability']}"
        if fn.get("outputs"):
            fn_str += f" returns {_format_params(fn['outputs'])}"
        fn_str += ";"
        result.append(fn_str)

    return result


def generate_interface(
    abi: List[Dict], interface_name: str, legacy_support: bool = False, indent: int = 4
) -> str:

    abi = deepcopy(abi)
    interface = f"pragma solidity >={'0.4.17' if legacy_support else '0.5.0'};"
    indent_str = f"\n{' ' * indent} "

    structs = generate_structs(abi)
    events = generate_events(abi)
    functions = generate_functions(abi)

    if structs:
        interface += f"\npragma experimental ABIEncoderV2;\n\n"
        interface += f"{'contract' if legacy_support else 'interface'} {interface_name} {{"
    else:
        interface += f"\n\ninterface {interface_name} {{"

    for content in [i for i in (structs, events, functions) if i]:
        for line in content:
            interface += f"{indent_str}{line}"
        interface += "\n"

    interface += "}"
    return interface
