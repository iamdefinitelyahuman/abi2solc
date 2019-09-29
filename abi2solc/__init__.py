#!/usr/bin/python3

from copy import deepcopy
from typing import Dict, List


def _format_param(param: Dict) -> str:
    formatted = param["type"]
    if param.get("indexed"):
        formatted += " indexed"
    if param.get("name"):
        formatted += f" {param['name']}"
    return formatted


def _format_params(params: List[Dict]) -> str:
    return f"({', '.join(_format_param(i) for i in params)})"


def _get_structs(params: List[Dict], struct_map: Dict) -> Dict:
    struct_abi = [i for i in params if "components" in i]

    for item in struct_abi:
        if [i for i in item["components"] if "components" in i]:
            _get_structs(item["components"], struct_map)
        s = tuple((i["name"], i["type"]) for i in item["components"])
        key = next((k for k, v in struct_map.items() if v == s), None)
        if not key:
            key = f"Tuple{len(struct_map)+1}"
            struct_map[key] = s
        item["type"] = item["type"].replace("tuple", key)

    return struct_map


def generate_interface(abi: List[Dict], interface_name: str, indent: int = 4) -> str:
    abi = deepcopy(abi)
    interface = f"pragma solidity >=0.4.22;\n\ninterface {interface_name} {{"
    indent_str = " " * indent

    structs: Dict = {}
    for item in abi:
        params = item.get("inputs", []) + item.get("outputs", [])
        _get_structs(params, structs)

    for key, value in structs.items():
        value = " ".join(f"{i[1]} {i[0]};" for i in value)
        interface += f"\n{indent_str}struct {key} {{ {value} }}"
    if structs:
        interface += "\n"

    events_abi = sorted([i for i in abi if i["type"] == "event"], key=lambda k: k["name"])
    for event in events_abi:
        interface += f"\n{indent_str}event {event['name']} "
        interface += f"{_format_params(event['inputs'])};"
    if events_abi:
        interface += "\n"

    fn_abi = sorted(
        [i for i in abi if i["type"] in ("function", "fallback")],
        key=lambda k: (k["stateMutability"], k.get("name", "")),
    )
    for fn in fn_abi:
        interface += f"\n{indent_str}function "
        if fn.get("name"):
            interface += f"{fn['name']} "
        interface += _format_params(fn.get("inputs", []))
        interface += " external"
        if fn["stateMutability"] != "nonpayable":
            interface += f" {fn['stateMutability']}"
        if fn.get("outputs"):
            interface += f" returns {_format_params(fn['outputs'])}"
        interface += ";"

    interface += "\n}"
    return interface
