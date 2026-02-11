#!/usr/bin/env python3
import json
import os
from pathlib import Path
from datetime import datetime, timezone
import yaml

QUEUE = Path('/root/.openclaw/workspace/agent-teams/task_queue.yaml')
AGENTS_ROOT = Path('/root/.openclaw/agents')

OWNERS = ['coordinator', 'engineer', 'researcher', 'qa']
STALE_MIN = 20


def now_utc():
    return datetime.now(timezone.utc)


def latest_agent_activity(owner: str):
    sessions = AGENTS_ROOT / owner / 'sessions'
    if not sessions.exists():
        return None
    latest = None
    for f in sessions.glob('*.jsonl'):
        ts = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
        if latest is None or ts > latest:
            latest = ts
    return latest


def main():
    if not QUEUE.exists():
        print('NO_QUEUE')
        return

    data = yaml.safe_load(QUEUE.read_text()) or {}
    tasks = data.get('tasks', [])
    now = now_utc()

    activity = {o: latest_agent_activity(o) for o in OWNERS}
    alerts = []

    for t in tasks:
        owner = (t.get('owner') or '').strip()
        status = (t.get('status') or '').strip().lower()
        prio = (t.get('priority') or 'medium').strip().lower()

        if owner in activity and activity[owner] is not None:
            dt = activity[owner]
            mins = int((now - dt).total_seconds() // 60)
            t['last_active_at'] = dt.isoformat()
            t['execution_state'] = 'active' if mins < 3 else 'idle'
            t['idle_minutes'] = mins

            if status == 'in_progress' and mins >= STALE_MIN and prio in ('critical', 'high'):
                t['stale_in_progress'] = True
                alerts.append(f"{t.get('task_id')} ({owner}) stale {mins}m")
            else:
                t['stale_in_progress'] = False
        else:
            t['execution_state'] = 'unknown'
            t['last_active_at'] = None
            t['idle_minutes'] = None
            if status == 'in_progress' and prio in ('critical', 'high'):
                t['stale_in_progress'] = True
                alerts.append(f"{t.get('task_id')} ({owner}) no activity source")

    data['tasks'] = tasks
    QUEUE.write_text(yaml.safe_dump(data, sort_keys=False))

    summary = {
        'checked_at': now.isoformat(),
        'alerts': alerts,
        'total_tasks': len(tasks),
    }
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()
