# sandbox_runner.py
# Runs and tests generated code

import subprocess

def run_test(code: str, filename="temp_test.py"):
    with open(filename, "w") as f:
        f.write(code)
    try:
        result = subprocess.run(["python3", filename], capture_output=True, text=True, timeout=10)
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)