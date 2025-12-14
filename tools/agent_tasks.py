# agent_tasks.py
from wallet_loader import load_wallet
from tx_signer import send_tx
from contract_deployer import deploy_hello_agent, load_contract_address
from chain_config import RPC_ENDPOINTS
from web3 import Web3


def get_balance(chain: str):
    address, private_key = load_wallet()
    w3 = Web3(Web3.HTTPProvider(RPC_ENDPOINTS[chain]))
    bal = w3.eth.get_balance(address)
    return bal / 10**18


def run_autonomous_tasks():
    print("Agent Polygon Balance:", get_balance("polygon"))

    # 1) CONTRACT ADRESSE LADEN
    contract_addr = load_contract_address()

    # 2) FALLS NICHT VORHANDEN → DEPLOY
    if contract_addr is None:
        print("📢 Deploying HelloAgent contract…")
        contract_addr = deploy_hello_agent("polygon")
        print("Contract deployed at:", contract_addr)
    else:
        print("📦 Contract already deployed at:", contract_addr)

    # 3) TESTTRANSAKTION
    print("📢 Sending micro payment to test address…")

    tx = send_tx(
        chain="polygon",
        to="0x000000000000000000000000000000000000dEaD",
        amount_eth=0.001
    )

    print("Micro TX hash:", tx)
    return True
