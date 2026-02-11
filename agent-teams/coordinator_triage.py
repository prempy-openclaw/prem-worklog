#!/usr/bin/env python3
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


def main():
    data = load()
    tasks = data.get("tasks", [])
    triaged = 0

    for t in tasks:
        if t.get("status") == "todo":
            t["status"] = "in_progress"
            t["updated_at"] = now_iso()
            triaged += 1

    save(data)
    print(f"PASS: triaged {triaged} task(s) from todo -> in_progress")


if __name__ == "__main__":
    main()
