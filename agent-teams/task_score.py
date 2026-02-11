#!/usr/bin/env python3
import yaml
from pathlib import Path

QUEUE = Path('/root/.openclaw/workspace/agent-teams/task_queue.yaml')


def score_task(t):
    score = 0
    priority = str(t.get('priority', 'medium')).lower()
    status = str(t.get('status', 'todo')).lower()
    reopen = int(t.get('reopen_count', 0) or 0)
    critical = int(t.get('critical_open', 0) or 0)

    score += {'low': 1, 'medium': 3, 'high': 5}.get(priority, 3)
    if status == 'blocked':
        score += 4
    if status == 'in_progress':
        score += 2
    score += min(reopen, 3)
    score += critical * 3
    return score


def main():
    if not QUEUE.exists():
        print('No task queue found.')
        return

    data = yaml.safe_load(QUEUE.read_text()) or {'tasks': []}
    tasks = data.get('tasks', [])

    for t in tasks:
        t['score'] = score_task(t)

    tasks.sort(key=lambda x: x.get('score', 0), reverse=True)
    data['tasks'] = tasks
    QUEUE.write_text(yaml.safe_dump(data, sort_keys=False))

    print('PASS: task scores updated (descending)')
    for t in tasks[:5]:
        print(f"- {t.get('task_id')} | score={t.get('score')} | owner={t.get('owner')} | status={t.get('status')}")


if __name__ == '__main__':
    main()
