from web3 import Web3
from wallet_loader import load_wallet
from chain_config import MULTICHAIN_CONFIG


def send_tx(chain: str, to: str, amount_eth: float):
    address, private_key = load_wallet()

    cfg = MULTICHAIN_CONFIG[chain]
    w3 = Web3(Web3.HTTPProvider(cfg["rpc"]))

    # Nonce korrekt holen
    nonce = w3.eth.get_transaction_count(address)

    # Gaspreis deutlich erhöhen, damit kein "underpriced" Fehler kommt
    base_gas = w3.eth.gas_price
    gas_price = int(base_gas * 1.25)   # 25% höher

    tx = {
        "nonce": nonce,
        "to": to,
        "value": w3.to_wei(amount_eth, "ether"),
        "gas": 21000,
        "gasPrice": gas_price,
        "chainId": cfg["chain_id"],
        "from": address,
    }

    signed = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    return tx_hash.hex()
