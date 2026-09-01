"""Read public Base chain state without signing, spending, or using secrets."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import requests

BASE_RPC_URL = "https://mainnet.base.org"
PROJECT_WALLET = "0xebDEB0c5F371C70c0a592fBd8B9f19a7da994bBD"
USDC_CONTRACT = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"


def _rpc(method: str, params: list[Any]) -> str:
    response = requests.post(
        BASE_RPC_URL,
        json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params},
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()
    if "error" in payload:
        raise RuntimeError(payload["error"])
    return payload["result"]


def eth_balance(address: str = PROJECT_WALLET) -> Decimal:
    wei = int(_rpc("eth_getBalance", [address, "latest"]), 16)
    return Decimal(wei) / Decimal(10**18)


def usdc_balance(address: str = PROJECT_WALLET) -> Decimal:
    # ERC-20 balanceOf(address): 0x70a08231 + left-padded address.
    data = "0x70a08231" + address.lower().removeprefix("0x").rjust(64, "0")
    raw = _rpc("eth_call", [{"to": USDC_CONTRACT, "data": data}, "latest"])
    return Decimal(int(raw, 16)) / Decimal(10**6)


def base_snapshot(address: str = PROJECT_WALLET) -> dict[str, str]:
    return {
        "network": "Base mainnet",
        "address": address,
        "eth": str(eth_balance(address)),
        "usdc": str(usdc_balance(address)),
        "note": "Read-only RPC call; no signature, no transaction, no spend.",
    }
