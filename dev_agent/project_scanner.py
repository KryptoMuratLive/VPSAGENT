# project_scanner.py
import os
import datetime
import shutil

def scan_project(root_path):
    """
    Offizielle Scan-Funktion für den Meta-Controller.
    Durchsucht rekursiv alle Python-Dateien und gibt
    eine strukturierte Antwort zurück.
    """
    files = list_python_files(root_path)

    return {
        "files": files,
        "total_files": len(files),
        "root": root_path
    }

def list_python_files(root_path):
    python_files = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(".py") and not file.startswith('.'):
                full_path = os.path.join(root, file)
                python_files.append(full_path)
    return python_files

def backup_file(file_path, backup_root=".backup"):
    if not os.path.exists(backup_root):
        os.makedirs(backup_root)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.basename(file_path)
    backup_path = os.path.join(backup_root, f"{filename}_{timestamp}")
    shutil.copy(file_path, backup_path)
    return backup_path

if __name__ == "__main__":
    project_root = input("🔍 Ordner für Scan angeben (z.B. ../main_orchestrator): ").strip()
    files = list_python_files(project_root)
    print("\n📄 Gefundene Python-Dateien:\n")
    for f in files:
        print(f)
    
    if input("\n🔐 Backup ALLER Dateien? (y/n): ").lower().startswith("y"):
        for f in files:
            backup = backup_file(f)
            print(f"✅ Backup erstellt: {backup}")
