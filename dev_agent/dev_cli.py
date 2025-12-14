# /root/dev_gpt_builder/dev_cli.py

import sys
from meta_dev_controller import MetaDevController

def main():
    ctrl = MetaDevController(project_root="/root/gpt_bot")

    if len(sys.argv) < 2:
        print("Usage: python dev_cli.py [status|scan|drypatch|requestpatch|approve|deploy]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "status":
        print(ctrl.system_status())

    elif cmd == "scan":
        print(ctrl.scan_project())

    elif cmd == "drypatch":
        instr = " ".join(sys.argv[2:]) or input("GPT-Instruktion: ")
        print(ctrl.patch_dry_run(instr))

    elif cmd == "requestpatch":
        instr = " ".join(sys.argv[2:]) or input("GPT-Instruktion: ")
        print(ctrl.request_live_patch(instr))

    elif cmd == "approve":
        if len(sys.argv) < 3:
            print("Bitte Action-ID angeben.")
            sys.exit(1)
        action_id = sys.argv[2]
        print(ctrl.approve_action(action_id))

    elif cmd == "deploy":
        print(ctrl.deploy())

    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
