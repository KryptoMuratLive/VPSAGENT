import json
from web3 import Web3
from chain_config import MULTICHAIN_CONFIG

WALLET_FILE = "/root/dev_gpt_builder/state/agent_wallet.json"

def load_wallet():
    """Gibt (address, private_key) zurück – immer in dieser Reihenfolge."""
    with open(WALLET_FILE) as f:
        wallet = json.load(f)
    return wallet["address"], wallet["private_key"]

def get_web3(chain_name):
    cfg = MULTICHAIN_CONFIG[chain_name]
    w3 = Web3(Web3.HTTPProvider(cfg["rpc"]))
    return w3, cfg["chain_id"]

def check_balance(chain_name):
    address, _ = load_wallet()
    w3, _ = get_web3(chain_name)
    return w3.eth.get_balance(address)
