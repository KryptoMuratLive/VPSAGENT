# system_scanner.py
# Scans current running modules and checks their status

def scan_services():
    services = {
        "dispatcher": 8001,
        "rpc_worker_1": 8002,
        "rpc_worker_2": 8003,
        "analyzer": 8004,
        "orchestrator": 8005
    }
    results = {}
    for name, port in services.items():
        # simulate scan (in real case: use requests.get(f"http://localhost:{port}/health"))
        results[name] = "running"
    return results