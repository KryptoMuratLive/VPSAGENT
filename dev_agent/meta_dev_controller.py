# /root/dev_gpt_builder/meta_dev_controller.py

import json
import time
from pathlib import Path

# existierende Module aus deinem Dev-Stack:
import project_scanner
import batch_patch_runner
import patch_debug_runner
import sandbox_runner
import deploy_interface
from telegram_alert import send_alert

STATE_DIR = Path(__file__).parent / "state"
STATE_DIR.mkdir(exist_ok=True)
ACTIONS_FILE = STATE_DIR / "actions.json"
STATUS_FILE = STATE_DIR / "last_status.json"


class MetaDevController:
    """
    Orchestriert alle DEV-GPT-Operationen:
    - Scan
    - Patch (Dry-Run / Live)
    - Sandbox-Tests
    - Deploy
    - Status & Logging
    - Approval-Flow
    """

    def __init__(self, project_root="/root/gpt_bot"):
        self.project_root = Path(project_root)
        self._ensure_state_files()

    # ----------------- State-Handling -----------------

    def _ensure_state_files(self):
        if not ACTIONS_FILE.exists():
            ACTIONS_FILE.write_text("[]", encoding="utf-8")
        if not STATUS_FILE.exists():
            STATUS_FILE.write_text("{}", encoding="utf-8")

    def _load_actions(self):
        return json.loads(ACTIONS_FILE.read_text(encoding="utf-8") or "[]")

    def _save_actions(self, actions):
        ACTIONS_FILE.write_text(json.dumps(actions, indent=2), encoding="utf-8")

    def _append_action(self, action):
        actions = self._load_actions()
        actions.append(action)
        self._save_actions(actions)

    def _save_status(self, status: dict):
        STATUS_FILE.write_text(json.dumps(status, indent=2), encoding="utf-8")

    # ----------------- High-Level-API -----------------

    def system_status(self) -> dict:
        """
        Liefert kompakten Status für CLI / API.
        Hier kannst du später Orchestrator/Worker-Checks ergänzen.
        """
        status = {
            "project_root": str(self.project_root),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "pending_actions": [
                a for a in self._load_actions() if a.get("status") == "pending"
            ],
        }
        self._save_status(status)
        return status

    def scan_project(self) -> dict:
        """
        Nutzt dein project_scanner-Modul.
        """
        result = project_scanner.scan_project(str(self.project_root))
        action = {
            "type": "SCAN",
            "timestamp": time.time(),
            "status": "done",
            "details": {"files_found": len(result.get("files", []))}
        }
        self._append_action(action)
        return {"ok": True, "files_found": len(result.get("files", []))}

    def patch_dry_run(self, gpt_instruction: str) -> dict:
        """
        Dry-Run Patch: nutzt z.B. patch_debug_runner.
        Kein Live-Write im gpt_bot.
        """
        action = {
            "id": f"dryrun-{int(time.time())}",
            "type": "PATCH_DRY_RUN",
            "instruction": gpt_instruction,
            "status": "running",
        }
        self._append_action(action)

        try:
            result = patch_debug_runner.run_dry_patch(
                project_root=str(self.project_root),
                instruction=gpt_instruction
            )
            action["status"] = "done"
            action["result"] = result
            self._append_action(action)
            return {"ok": True, "result": result, "action_id": action["id"]}
        except Exception as e:
            action["status"] = "error"
            action["error"] = str(e)
            self._append_action(action)
            send_alert(f"[DEV-META] Dry-Run Patch Fehler: {e}")
            return {"ok": False, "error": str(e)}

    def request_live_patch(self, gpt_instruction: str) -> dict:
        """
        Legt eine pending Action an, die DU erst freigibst.
        """
        action_id = f"patch-{int(time.time())}"
        action = {
            "id": action_id,
            "type": "PATCH_LIVE",
            "instruction": gpt_instruction,
            "status": "pending",
            "created_at": time.time(),
        }
        self._append_action(action)

        # Telegram: Hinweis auf Freigabe
        send_alert(
            f"[DEV-META] Neue Patch-Anfrage:\n\n"
            f"ID: {action_id}\n"
            f"Instruktion:\n{gpt_instruction}\n\n"
            f"Freigeben auf dem Server mit:\n"
            f"  python dev_cli.py approve {action_id}"
        )

        return {"ok": True, "action_id": action_id}

    def approve_action(self, action_id: str) -> dict:
        """
        Wird von CLI aufgerufen: gibt einen pending PATCH_LIVE frei und führt ihn aus.
        """
        actions = self._load_actions()
        target = None
        for a in actions:
            if a.get("id") == action_id:
                target = a
                break

        if not target:
            return {"ok": False, "error": "Action not found"}

        if target.get("status") != "pending":
            return {"ok": False, "error": f"Action status is {target.get('status')}"}

        instr = target["instruction"]

        try:
            # hier nutzt du deinen echten Batch-Patcher
            result = batch_patch_runner.run_batch_patch(
                project_root=str(self.project_root),
                instruction=instr
            )
            target["status"] = "done"
            target["result"] = result
            self._save_actions(actions)

            send_alert(f"[DEV-META] Patch {action_id} erfolgreich ausgeführt.")
            return {"ok": True, "result": result}
        except Exception as e:
            target["status"] = "error"
            target["error"] = str(e)
            self._save_actions(actions)
            send_alert(f"[DEV-META] Patch {action_id} FEHLGESCHLAGEN: {e}")
            return {"ok": False, "error": str(e)}

    def sandbox_test(self, file_path: str) -> dict:
        """
        Nutzt sandbox_runner, um eine Datei / ein Modul isoliert zu testen.
        """
        try:
            result = sandbox_runner.run_in_sandbox(file_path)
            self._append_action({
                "type": "SANDBOX",
                "file": file_path,
                "status": "done",
                "result": result,
                "timestamp": time.time(),
            })
            return {"ok": True, "result": result}
        except Exception as e:
            send_alert(f"[DEV-META] Sandbox-Fehler in {file_path}: {e}")
            return {"ok": False, "error": str(e)}

    def deploy(self) -> dict:
        """
        Nutzt deploy_interface, um geprüfte Files ins Live-System zu schieben.
        """
        try:
            result = deploy_interface.deploy_project(str(self.project_root))
            self._append_action({
                "type": "DEPLOY",
                "status": "done",
                "timestamp": time.time(),
                "result": result,
            })
            send_alert("[DEV-META] Deployment erfolgreich abgeschlossen.")
            return {"ok": True, "result": result}
        except Exception as e:
            send_alert(f"[DEV-META] Deployment-Fehler: {e}")
            return {"ok": False, "error": str(e)}
