#!/usr/bin/env python3
import sys
import yaml
from datetime import datetime, timezone
from pathlib import Path

QUEUE = Path('/root/.openclaw/workspace/agent-teams/task_queue.yaml')


def load():
    if not QUEUE.exists():
        return {"tasks": [], "locks": {}}
    return yaml.safe_load(QUEUE.read_text()) or {"tasks": [], "locks": {}}


def save(data):
    QUEUE.write_text(yaml.safe_dump(data, sort_keys=False))


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def main():
    if len(sys.argv) < 3:
        print("Usage: claim_task.py <task_id> <owner>")
        sys.exit(1)

    task_id, owner = sys.argv[1], sys.argv[2]
    data = load()
    locks = data.setdefault("locks", {})
    tasks = data.setdefault("tasks", [])

    existing_owner = locks.get(task_id)
    if existing_owner and existing_owner != owner:
        print(f"FAIL: task {task_id} is locked by {existing_owner}")
        sys.exit(2)

    locks[task_id] = owner

    found = False
    for t in tasks:
        if t.get("task_id") == task_id:
            t["owner"] = owner
            t["updated_at"] = now_iso()
            found = True
            break

    if not found:
        tasks.append({
            "task_id": task_id,
            "title": "<add title>",
            "owner": owner,
            "status": "in_progress",
            "priority": "medium",
            "updated_at": now_iso(),
        })

    save(data)
    print(f"PASS: {owner} claimed {task_id}")


if __name__ == '__main__':
    main()
