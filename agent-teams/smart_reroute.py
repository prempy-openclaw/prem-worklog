#!/usr/bin/env python3
import yaml
from pathlib import Path

QUEUE = Path('/root/.openclaw/workspace/agent-teams/task_queue.yaml')


def main():
    if not QUEUE.exists():
        print('No task queue found.')
        return

    data = yaml.safe_load(QUEUE.read_text()) or {'tasks': [], 'locks': {}}
    tasks = data.get('tasks', [])
    locks = data.setdefault('locks', {})

    rerouted = []
    for t in tasks:
        title = str(t.get('title', '')).lower()
        owner = t.get('owner')
        if t.get('status') == 'blocked' and owner == 'engineer':
            t['owner'] = 'coordinator'
            locks[t.get('task_id')] = 'coordinator'
            rerouted.append((t.get('task_id'), 'engineer', 'coordinator', 'blocked escalation'))
        elif ('research' in title or 'benchmark' in title) and owner not in ('researcher', 'coordinator'):
            t['owner'] = 'researcher'
            locks[t.get('task_id')] = 'researcher'
            rerouted.append((t.get('task_id'), owner, 'researcher', 'topic match'))

    QUEUE.write_text(yaml.safe_dump(data, sort_keys=False))

    if not rerouted:
        print('PASS: no reroute needed')
    else:
        print('PASS: rerouted tasks')
        for tid, src, dst, reason in rerouted:
            print(f'- {tid}: {src} -> {dst} ({reason})')


if __name__ == '__main__':
    main()
