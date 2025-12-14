from eth_account import Account
import json

def create_wallet():
    acct = Account.create()

    data = {
        "address": acct.address,
        "private_key": acct.key.hex()
    }

    # Wallet wird im state/ Ordner gespeichert
    with open("/root/dev_gpt_builder/state/agent_wallet.json", "w") as f:
        json.dump(data, f, indent=4)

    print("\n✅ EVM-Agent-Wallet erfolgreich erstellt")
    print("Adresse:", data["address"])
    print("Private Key:", data["private_key"])
    print("\n⚠️ WICHTIG: Private Key niemals weitergeben!\n")

if __name__ == "__main__":
    create_wallet()
