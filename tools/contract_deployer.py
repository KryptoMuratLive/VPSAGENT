# contract_deployer.py
import json
import os
from web3 import Web3
from solcx import compile_source
from chain_config import RPC_ENDPOINTS
from wallet_loader import load_wallet

STATE_FILE = "/root/dev_gpt_builder/state/deployed_contract.json"

HELLO_CONTRACT = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract HelloAgent {
    string public message = "Hello from autonomous agent";

    function setMessage(string memory newMsg) public {
        message = newMsg;
    }
}
"""

def save_contract_address(addr: str):
    data = {"address": addr}
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)

def load_contract_address():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f).get("address")
    return None


def deploy_hello_agent(chain: str) -> str:
    """Deployt den Contract nur, wenn er noch nicht existiert."""
    
    # FIX: Reihenfolge korrigiert!
    address, private_key = load_wallet()

    w3 = Web3(Web3.HTTPProvider(RPC_ENDPOINTS[chain]))
    assert w3.is_connected(), "RPC not reachable"

    compiled = compile_source(HELLO_CONTRACT, output_values=["abi", "bin"])
    contract_id, contract_interface = compiled.popitem()
    abi = contract_interface["abi"]
    bytecode = contract_interface["bin"]

    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    nonce = w3.eth.get_transaction_count(address)
    gas_price = int(w3.eth.gas_price * 1.1)

    tx = contract.constructor().build_transaction({
        "from": address,
        "nonce": nonce,
        "gasPrice": gas_price,
    })

    signed = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    contract_address = receipt.contractAddress
    save_contract_address(contract_address)

    return contract_address
