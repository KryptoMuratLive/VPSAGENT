# /root/dev_gpt_builder/dev_api.py

from flask import Flask, request, jsonify
from meta_dev_controller import MetaDevController

app = Flask(__name__)
ctrl = MetaDevController(project_root="/root/gpt_bot")

@app.get("/status")
def status():
    return jsonify(ctrl.system_status())

@app.post("/scan")
def scan():
    return jsonify(ctrl.scan_project())

@app.post("/drypatch")
def drypatch():
    data = request.get_json(force=True)
    instr = data.get("instruction", "")
    return jsonify(ctrl.patch_dry_run(instr))

@app.post("/requestpatch")
def requestpatch():
    data = request.get_json(force=True)
    instr = data.get("instruction", "")
    return jsonify(ctrl.request_live_patch(instr))

@app.post("/approve")
def approve():
    data = request.get_json(force=True)
    action_id = data.get("action_id")
    return jsonify(ctrl.approve_action(action_id))

@app.post("/deploy")
def deploy():
    return jsonify(ctrl.deploy())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8010)
