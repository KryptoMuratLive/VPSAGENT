# airdrop_farmer.py
import json
import os
from datetime import datetime
from web3 import Web3
from wallet_loader import load_wallet
from chain_config import MULTICHAIN_CONFIG

LOG_FILE = "/root/dev_gpt_builder/state/airdrop_log.txt"
GAS_TRACK_FILE = "/root/dev_gpt_builder/state/gas_spent.json"

MONTHLY_GAS_LIMIT = 2.0      # Gesamtbudget
TX_AMOUNT = 0.0004           # Self-TX Betrag


# ------------------------------------------------------------
def log(msg: str):
    ts = datetime.utcnow().isoformat()
    line = f"[{ts}] {msg}"
    print(line)
    os.makedirs("/root/dev_gpt_builder/state", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


# ------------------------------------------------------------
def load_gas():
    try:
        with open(GAS_TRACK_FILE, "r") as f:
            return json.load(f)
    except:
        return {"month": datetime.utcnow().month, "spent": 0.0}


def save_gas(v: float):
    with open(GAS_TRACK_FILE, "w") as f:
        json.dump({"month": datetime.utcnow().month, "spent": v}, f)


# ------------------------------------------------------------
def perform_chain_activity(chain: str):
    address, private_key = load_wallet()
    cfg = MULTICHAIN_CONFIG[chain]

    # Web3 Objekt bauen
    try:
        w3 = Web3(Web3.HTTPProvider(cfg["rpc"]))
    except Exception as e:
        log(f"[{chain}] ❌ RPC Fehler beim Initialisieren: {e}")
        return False

    # RPC erreichbar?
    if not w3.is_connected():
        log(f"[{chain}] ❌ RPC nicht erreichbar.")
        return False

    # Balance abrufen
    try:
        bal = w3.eth.get_balance(address) / 10**cfg["decimals"]
    except Exception as e:
        log(f"[{chain}] ❌ Balance Fehler: {e}")
        return False

    log(f"[{chain}] Balance: {bal:.6f} {cfg['symbol']}")

    if bal <= 0:
        log(f"[{chain}] ⚠️ Kein Gas – überspringe.")
        return False

    # Gasbudget
    gas_data = load_gas()
    now = datetime.utcnow().month

    if gas_data["month"] != now:
        gas_data = {"month": now, "spent": 0.0}
        save_gas(0.0)

    if gas_data["spent"] >= MONTHLY_GAS_LIMIT:
        log(f"[{chain}] ⚠️ Monatsgaslimit erreicht.")
        return False

    # TX vorbereiten
    try:
        nonce = w3.eth.get_transaction_count(address)
        gas_price = int(w3.eth.gas_price * 1.12)
    except Exception as e:
        log(f"[{chain}] ❌ Fehler beim Gas/NONCE: {e}")
        return False

    tx = {
        "from": address,
        "to": address,
        "value": w3.to_wei(TX_AMOUNT, "ether"),
        "gas": 90000,
        "gasPrice": gas_price,
        "nonce": nonce,
        "chainId": cfg["chain_id"],
    }

    try:
        signed = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        log(f"[{chain}] TX hash: {tx_hash.hex()}")
    except Exception as e:
        log(f"[{chain}] ❌ TX Fehler: {e}")
        return False

    # Gasverbrauch aktualisieren
    gas_data["spent"] += 0.00035
    save_gas(gas_data["spent"])

    return True


# ------------------------------------------------------------
def run_airdrop_cycle():
    log("🚀 Starte Multi-Chain Cycle...")

    CHAINS = [
    "ethereum",
    "polygon",
    "bsc",
    "arbitrum",
    "optimism",
    "base",
    "linea",
    "zksync",
    "scroll"
]
    result = {}

    for chain in CHAINS:
        log(f"--- {chain.upper()} ---")
        try:
            result[chain] = perform_chain_activity(chain)
        except Exception as e:
            log(f"[{chain}] ❌ Unerwarteter Fehler: {e}")
            result[chain] = False

    log("🧾 Zyklus abgeschlossen.")
    return result
