#!/usr/bin/env python3
import yaml
from pathlib import Path
from collections import defaultdict

QUEUE = Path('/root/.openclaw/workspace/agent-teams/task_queue.yaml')


def main():
    if not QUEUE.exists():
        print("No task queue found.")
        return

    data = yaml.safe_load(QUEUE.read_text()) or {}
    tasks = data.get('tasks', [])

    by_owner = defaultdict(list)
    blocked = []
    for t in tasks:
        owner = t.get('owner', 'unassigned')
        by_owner[owner].append(t)
        if t.get('status') == 'blocked':
            blocked.append(t)

    print("🤖 Agent Team Daily Standup")
    print("")
    for owner, items in sorted(by_owner.items()):
        open_items = [x for x in items if x.get('status') != 'done']
        print(f"- {owner}: {len(open_items)} open / {len(items)} total")
        for t in open_items[:3]:
            print(f"  • {t.get('task_id')} | {t.get('status')} | {t.get('title')}")

    print("")
    if blocked:
        print("🚨 Blocked tasks:")
        for t in blocked:
            print(f"- {t.get('task_id')} ({t.get('owner')}): {t.get('title')}")
    else:
        print("✅ No blocked tasks")


if __name__ == '__main__':
    main()
