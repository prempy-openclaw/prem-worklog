#!/usr/bin/env python3
import yaml
from pathlib import Path
from datetime import datetime, timezone

QUEUE = Path('/root/.openclaw/workspace/agent-teams/task_queue.yaml')
THRESHOLD_MIN = 15


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
    now = datetime.now(timezone.utc)

    escalated = []
    for t in tasks:
        if t.get('status') != 'blocked':
            continue
        updated = parse_iso(t.get('updated_at'))
        if not updated:
            continue
        age_min = (now - updated).total_seconds() / 60
        if age_min > THRESHOLD_MIN and not t.get('escalated', False):
            t['escalated'] = True
            t['escalated_at'] = now.replace(microsecond=0).isoformat()
            escalated.append((t.get('task_id'), t.get('owner'), t.get('title'), age_min))

    QUEUE.write_text(yaml.safe_dump(data, sort_keys=False))

    if not escalated:
        print('✅ No blocked tasks requiring escalation.')
        return

    print('🚨 Blocked task escalations (>15m)')
    for tid, owner, title, age in escalated:
        print(f'- {tid} | owner={owner} | age={age:.1f}m | {title}')


if __name__ == '__main__':
    main()
