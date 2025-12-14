# multi_file_editor.py
import os
from project_scanner import list_python_files, backup_file
from openai_client import generate_code_with_gpt

def apply_patch_to_file(file_path, instruction):
    with open(file_path, "r", encoding="utf-8") as f:
        original_code = f.read()

    prompt = (
        f"Bitte ändere die folgende Python-Datei basierend auf dieser Anweisung:\n"
        f"{instruction}\n\n"
        f"---\nOriginalcode:\n{original_code}\n---\n"
        f"Gib ausschließlich den neuen vollständigen Python-Code zurück."
    )

    patched_code = generate_code_with_gpt(prompt)
    if not patched_code or len(patched_code) < 10:
        print(f"❌ Kein gültiger Patch von GPT für {file_path}")
        return

    backup_path = backup_file(file_path)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(patched_code)

    print(f"✅ Datei aktualisiert: {file_path}")
    print(f"🔒 Backup gespeichert unter: {backup_path}")

if __name__ == "__main__":
    target_folder = input("📁 Zu bearbeitender Ordner (z.B. ../main_orchestrator): ").strip()
    task = input("🧠 Was soll DEV GPT tun (z. B. Funktion einbauen)? ").strip()

    files = list_python_files(target_folder)
    for file in files:
        print(f"\n🔧 Datei: {file}")
        if input("→ Diese Datei patchen? (y/n): ").lower().startswith("y"):
            apply_patch_to_file(file, task)
