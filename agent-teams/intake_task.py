#!/usr/bin/env python3
import sys
import yaml
from pathlib import Path
from datetime import datetime, timezone

QUEUE = Path('/root/.openclaw/workspace/agent-teams/task_queue.yaml')


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load():
    if not QUEUE.exists():
        return {"tasks": [], "locks": {}}
    return yaml.safe_load(QUEUE.read_text()) or {"tasks": [], "locks": {}}


def save(data):
    QUEUE.write_text(yaml.safe_dump(data, sort_keys=False))


def guess_owner(title: str):
    t = title.lower()
    if any(k in t for k in ["bug", "fix", "implement", "api", "code", "test"]):
        return "engineer"
    if any(k in t for k in ["research", "benchmark", "compare", "insight"]):
        return "researcher"
    if any(k in t for k in ["verify", "qa", "regression", "validate"]):
        return "qa"
    return "coordinator"


def main():
    if len(sys.argv) < 3:
        print("Usage: intake_task.py <task_id> <title> [priority]")
        sys.exit(1)

    task_id = sys.argv[1]
    title = sys.argv[2]
    priority = sys.argv[3] if len(sys.argv) > 3 else "medium"

    data = load()
    owner = guess_owner(title)

    task = {
        "task_id": task_id,
        "title": title,
        "owner": owner,
        "status": "todo",
        "priority": priority,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "reopen_count": 0,
    }

    data.setdefault("tasks", []).append(task)
    data.setdefault("locks", {})[task_id] = owner
    save(data)

    print(f"PASS: task {task_id} created | owner={owner} | priority={priority}")


if __name__ == "__main__":
    main()
