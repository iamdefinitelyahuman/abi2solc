#!/usr/bin/python3

from typing import Dict, List, Tuple


def _format_param(param: Dict) -> str:
    formatted = param["type"]
    if param.get("indexed"):
        formatted += " indexed"
    if param.get("name"):
        formatted += f" {param['name']}"
    return formatted


def _format_params(params: List[Dict]) -> str:
    return f"({', '.join(_format_param(i) for i in params)})"


def generate_interface(abi: List[Dict], interface_name: str, indent: int = 4) -> str:
    interface = f"pragma solidity >=0.4.22;\n\ninterface {interface_name} {{"
    indent_str = " " * indent

    for event in sorted([i for i in abi if i["type"] == "event"], key=lambda k: k["name"]):
        interface += f"\n{indent_str}event {event['name']} "
        interface += f"{_format_params(event['inputs'])};"

    interface += "\n"

    for fn in sorted(
        [i for i in abi if i["type"] in ("function", "fallback")],
        key=lambda k: (k["stateMutability"], k.get("name", "")),
    ):
        interface += f"\n{indent_str}function "
        if fn.get('name'):
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
