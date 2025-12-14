# auto_integrator.py (Code extrahieren aus Markdown)
from code_generator import generate_code
from sandbox_runner import run_test
from deploy_interface import confirm_deploy
import re

def extract_code_blocks(text):
    # Sucht NUR nach Markdown-Codeblöcken (```python ... ```)
    match = re.search(r"```python\\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def run_auto_integration(feature_prompt):
    print(f"\n📥 Anforderung empfangen: {feature_prompt}\n")

    raw_output = generate_code(feature_prompt)
    code = extract_code_blocks(raw_output)

    if not code or len(code) < 10:
        print("\n❌ Kein gültiger Code erhalten. GPT hat wahrscheinlich nur Text geliefert.")
        print("\n🔎 Rohantwort:\n")
        print(raw_output)
        return

    print("\n📄 Verarbeiteter Code:\n")
    print(code)

    print("\n🧪 Starte Testlauf...")
    output, error = run_test(code)

    if error:
        print("\n❌ Fehler beim Ausführen des Codes:\n")
        print(error)
        return

    print("\n✅ Testausgabe:\n")
    print(output)

    if confirm_deploy(code):
        filename = feature_prompt.lower().replace(" ", "_").replace("-", "_") + ".py"
        with open(filename, "w") as f:
            f.write(code)
        print(f"\n📦 Modul gespeichert als: {filename}")
    else:
        print("\n⛔ Einbau abgebrochen.")

if __name__ == "__main__":
    prompt = input("Was soll gebaut werden? 🛠️  → ")
    run_auto_integration(prompt)
