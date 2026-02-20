#!/usr/bin/env python3
import yaml
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import Counter

QUEUE = Path('/root/.openclaw/workspace/agent-teams/task_queue.yaml')


def parse_iso(ts):
    try:
        return datetime.fromisoformat(str(ts).replace('Z', '+00:00'))
    except Exception:
        return None


def main():
    if not QUEUE.exists():
        print('No task queue found.')
        return

    data = yaml.safe_load(QUEUE.read_text()) or {}
    tasks = data.get('tasks', [])
    since = datetime.now(timezone.utc) - timedelta(days=7)

    done_recent = []
    by_owner = Counter()
    for t in tasks:
        if t.get('status') != 'done':
            continue
        updated = parse_iso(t.get('updated_at'))
        if updated and updated >= since:
            done_recent.append(t)
            by_owner[t.get('owner', 'unassigned')] += 1

    print('📈 Weekly Velocity (last 7d)')
    print(f'- completed_tasks: {len(done_recent)}')
    if by_owner:
        print('- by_owner:')
        for owner, count in sorted(by_owner.items()):
            print(f'  • {owner}: {count}')
    else:
        print('- by_owner: none')


if __name__ == '__main__':
    main()
