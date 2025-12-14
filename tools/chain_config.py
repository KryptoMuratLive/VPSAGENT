# chain_config.py
# Zentrale Multi-Chain-Konfiguration (sauber & erweiterbar)

# --------------------------------------------------
# RPC ENDPOINTS
# --------------------------------------------------
RPC_ENDPOINTS = {
    # Main Chains
    "ethereum": "https://rpc.ankr.com/eth/0ea4c60ce15618b04f3457dcb990b110adf492e42db0d51eacbf6ccdaca6e29b",

    # L2 / Sidechains
    "polygon":  "https://polygon-rpc.com",
    "bsc":      "https://bsc-dataseed.binance.org",

    # ANKR L2s
    "arbitrum": "https://rpc.ankr.com/arbitrum/0ea4c60ce15618b04f3457dcb990b110adf492e42db0d51eacbf6ccdaca6e29b",
    "optimism": "https://rpc.ankr.com/optimism/0ea4c60ce15618b04f3457dcb990b110adf492e42db0d51eacbf6ccdaca6e29b",
    "base":     "https://rpc.ankr.com/base/0ea4c60ce15618b04f3457dcb990b110adf492e42db0d51eacbf6ccdaca6e29b",

    # ZK / New L2
    "zksync":   "https://rpc.ankr.com/zksync_era/0ea4c60ce15618b04f3457dcb990b110adf492e42db0d51eacbf6ccdaca6e29b",
    "linea":    "https://rpc.ankr.com/linea/0ea4c60ce15618b04f3457dcb990b110adf492e42db0d51eacbf6ccdaca6e29b",
    "scroll":   "https://rpc.ankr.com/scroll/0ea4c60ce15618b04f3457dcb990b110adf492e42db0d51eacbf6ccdaca6e29b",
}

# --------------------------------------------------
# MULTI-CHAIN CONFIG
# --------------------------------------------------
MULTICHAIN_CONFIG = {

    # ---- MAIN ----
    "ethereum": {
        "rpc": RPC_ENDPOINTS["ethereum"],
        "chain_id": 1,
        "symbol": "ETH",
        "decimals": 18
    },

    # ---- SIDECHAINS ----
    "polygon": {
        "rpc": RPC_ENDPOINTS["polygon"],
        "chain_id": 137,
        "symbol": "MATIC",
        "decimals": 18
    },

    "bsc": {
        "rpc": RPC_ENDPOINTS["bsc"],
        "chain_id": 56,
        "symbol": "BNB",
        "decimals": 18
    },

    # ---- L2 ETH GAS ----
    "arbitrum": {
        "rpc": RPC_ENDPOINTS["arbitrum"],
        "chain_id": 42161,
        "symbol": "ETH",
        "decimals": 18
    },

    "optimism": {
        "rpc": RPC_ENDPOINTS["optimism"],
        "chain_id": 10,
        "symbol": "ETH",
        "decimals": 18
    },

    "base": {
        "rpc": RPC_ENDPOINTS["base"],
        "chain_id": 8453,
        "symbol": "ETH",
        "decimals": 18
    },

    # ---- ZK CHAINS ----
    "zksync": {
        "rpc": RPC_ENDPOINTS["zksync"],
        "chain_id": 324,
        "symbol": "ETH",
        "decimals": 18
    },

    "linea": {
        "rpc": RPC_ENDPOINTS["linea"],
        "chain_id": 59144,
        "symbol": "ETH",
        "decimals": 18
    },

    "scroll": {
        "rpc": RPC_ENDPOINTS["scroll"],
        "chain_id": 534352,
        "symbol": "ETH",
        "decimals": 18
    },
}
