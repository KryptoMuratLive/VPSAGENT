# deploy_interface.py
# Asks for user confirmation to deploy new module

def confirm_deploy(code: str):
    print("Generated Code:\n")
    print(code)
    answer = input("Einbauen? (y/n): ")
    return answer.lower().startswith("y")