#!/usr/bin/env python3
import yaml
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

QUEUE = Path('/root/.openclaw/workspace/agent-teams/task_queue.yaml')


def parse_iso(ts):
    try:
        return datetime.fromisoformat(ts.replace('Z', '+00:00'))
    except Exception:
        return None


def main():
    if not QUEUE.exists():
        print('No task queue found.')
        return

    data = yaml.safe_load(QUEUE.read_text()) or {}
    tasks = data.get('tasks', [])

    total = len(tasks)
    status_counts = Counter(t.get('status', 'unknown') for t in tasks)
    done = status_counts.get('done', 0)
    blocked = status_counts.get('blocked', 0)

    rework = sum(1 for t in tasks if int(t.get('reopen_count', 0) or 0) > 0)
    rework_rate = (rework / total * 100) if total else 0
    blocked_ratio = (blocked / total * 100) if total else 0

    now = datetime.now(timezone.utc)
    lead_times = []
    for t in tasks:
        created = parse_iso(str(t.get('created_at', '')))
        updated = parse_iso(str(t.get('updated_at', '')))
        if created and updated and t.get('status') == 'done':
            lead_times.append((updated - created).total_seconds() / 60)

    median_time = 0
    if lead_times:
        lead_times.sort()
        n = len(lead_times)
        median_time = lead_times[n // 2] if n % 2 == 1 else (lead_times[n//2 - 1] + lead_times[n//2]) / 2

    print('📊 Agent Team Metrics')
    print(f'- total_tasks: {total}')
    print(f'- done: {done}')
    print(f'- in_progress: {status_counts.get("in_progress", 0)}')
    print(f'- blocked: {blocked}')
    print(f'- blocked_ratio: {blocked_ratio:.1f}%')
    print(f'- rework_rate: {rework_rate:.1f}%')
    print(f'- median_time_to_done_min: {median_time:.1f}')


if __name__ == '__main__':
    main()
