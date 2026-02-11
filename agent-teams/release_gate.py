#!/usr/bin/env python3
import sys
import yaml
from pathlib import Path

QUEUE = Path('/root/.openclaw/workspace/agent-teams/task_queue.yaml')


def load():
    if not QUEUE.exists():
        return {"tasks": []}
    return yaml.safe_load(QUEUE.read_text()) or {"tasks": []}


def main():
    if len(sys.argv) < 2:
        print("Usage: release_gate.py <task_id>")
        sys.exit(1)

    task_id = sys.argv[1]
    data = load()
    tasks = data.get("tasks", [])

    task = next((t for t in tasks if t.get("task_id") == task_id), None)
    if not task:
        print(f"FAIL: task not found: {task_id}")
        sys.exit(2)

    qa_status = task.get("qa_status", "pending")
    verification_ok = bool(task.get("verification_pass", False))
    blocked = task.get("status") == "blocked"
    critical_open = int(task.get("critical_open", 0) or 0) > 0

    reasons = []
    if qa_status != "pass":
        reasons.append(f"qa_status={qa_status}")
    if not verification_ok:
        reasons.append("verification_pass=false")
    if blocked:
        reasons.append("status=blocked")
    if critical_open:
        reasons.append("critical_open>0")

    if reasons:
        print("FAIL: release gate blocked -> " + ", ".join(reasons))
        sys.exit(3)

    print("PASS: release gate passed")


if __name__ == "__main__":
    main()
