# batch_patch_runner.py mit sichtbarem Logging
from dependency_mapper import build_dependency_graph
from project_scanner import list_python_files, backup_file
from openai_client import generate_code_with_gpt
import os

def run_batch_patch(project_root, instruction):
    """
    Standardisierte Patch-Funktion für den Meta-Controller.
    Führt echte GPT-Patches durch, speichert Backups,
    und gibt ein strukturiertes Ergebnis zurück.
    """
    results = []
    files = list_python_files(project_root)

    # Dependency-Analyse (optional, aber vorhanden in deinem System)
    graph = build_dependency_graph(files)

    print("\n📊 Module erkannt:")
    for mod in graph:
        print(f" - {mod}")

    print("\n⚙️ Starte echten Patchlauf:\n")

    for file_path in files:
        try:
            patch_module(file_path, instruction)
            results.append({"file": file_path, "status": "ok"})
        except Exception as e:
            results.append({"file": file_path, "status": "error", "msg": str(e)})

    return {
        "total_files": len(results),
        "success": len([r for r in results if r["status"] == "ok"]),
        "errors": [r for r in results if r["status"] == "error"],
        "instruction": instruction,
        "project_root": project_root,
    }

def patch_module(file_path, instruction):
    print(f"\n🔧 Bearbeite Datei: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        original_code = f.read()

    prompt = (
        f"Ändere folgenden Python-Code basierend auf dieser Anweisung:\n"
        f"{instruction}\n\n"
        f"---\n{original_code}\n---\n"
        f"Gib ausschließlich den neuen vollständigen Python-Code zurück."
    )

    print("📤 Sende GPT-Anfrage...")
    patched = generate_code_with_gpt(prompt)

    if not patched or len(patched) < 10:
        print("❌ Keine gültige Antwort von GPT.")
        return

    backup = backup_file(file_path)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(patched)
    print(f"✅ Datei aktualisiert: {file_path}")
    print(f"🔒 Backup gespeichert unter: {backup}")

if __name__ == "__main__":
    project_root = input("📂 Projektordner (z. B. ../main_orchestrator): ").strip()
    instruction = input("🧠 Einmalige GPT-Anweisung: ").strip()

    files = list_python_files(project_root)
    graph = build_dependency_graph(files)

    print("\n📊 Erkannte Module:")
    for mod in graph:
        print(f"🧩 {mod}")

    print("\n⚙️ Starte automatische GPT-Patches...\n")
    for file_path in files:
        patch_module(file_path, instruction)
