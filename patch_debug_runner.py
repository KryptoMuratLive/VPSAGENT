import os
from openai_client import generate_code_with_gpt
from project_scanner import backup_file

def patch_file(file_path, instruction, log_file):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        prompt = (
            f"{instruction}\n\n"
            f"---\n{code}\n---\n"
            f"Gib ausschließlich den neuen vollständigen Python-Code zurück."
        )
        patched = generate_code_with_gpt(prompt)

        if not patched or len(patched) < 10:
            log_file.write(f"[SKIP] {file_path} – Keine gültige Antwort\n")
            return

        backup = backup_file(file_path)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(patched)
        log_file.write(f"[OK] {file_path} → Backup: {backup}\n")

    except Exception as e:
        log_file.write(f"[ERROR] {file_path} – {str(e)}\n")

def run_dry_patch(project_root, instruction):
    """
    Ultra-schneller Dry-Run:
    - Kein GPT
    - Keine Dateiänderung
    - Nur Simulation
    - Zeigt, welche Dateien betroffen wären
    """

    results = []
    for dirpath, _, filenames in os.walk(project_root):
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                results.append({"file": file_path, "status": "would_patch"})

    return {
        "total_files": len(results),
        "would_patch": len(results),
        "instruction": instruction,
        "details_preview": results[:10]
    }

if __name__ == "__main__":
    root_dir = input("📂 Projektordner: ").strip()
    instruction = input("🧠 GPT-Anweisung: ").strip()
    log_path = "patch_run.log"

    with open(log_path, "w", encoding="utf-8") as log_file:
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith(".py"):
                    full_path = os.path.join(dirpath, filename)
                    patch_file(full_path, instruction, log_file)

    print(f"📄 Patchlauf abgeschlossen. Logfile: {log_path}")
