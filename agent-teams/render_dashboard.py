#!/usr/bin/env python3
import yaml
from pathlib import Path
from collections import defaultdict

QUEUE = Path('/root/.openclaw/workspace/agent-teams/task_queue.yaml')
OUT = Path('/root/.openclaw/workspace/agent-teams/DASHBOARD.md')


def main():
    data = yaml.safe_load(QUEUE.read_text()) if QUEUE.exists() else {"tasks": []}
    tasks = data.get("tasks", [])

    by_owner = defaultdict(list)
    for t in tasks:
        by_owner[t.get("owner", "unassigned")].append(t)

    lines = ["# Agent Team Dashboard", "", "## Summary", ""]
    lines.append(f"- Total tasks: {len(tasks)}")
    lines.append(f"- Done: {sum(1 for t in tasks if t.get('status') == 'done')}")
    lines.append(f"- In progress: {sum(1 for t in tasks if t.get('status') == 'in_progress')}")
    lines.append(f"- Blocked: {sum(1 for t in tasks if t.get('status') == 'blocked')}")
    lines.append("")

    lines.append("## Tasks by Owner")
    lines.append("")
    for owner in sorted(by_owner.keys()):
        lines.append(f"### {owner}")
        lines.append("")
        lines.append("| Task ID | Status | Priority | Title |")
        lines.append("|---|---|---|---|")
        for t in by_owner[owner]:
            lines.append(f"| {t.get('task_id')} | {t.get('status')} | {t.get('priority')} | {t.get('title')} |")
        lines.append("")

    OUT.write_text("\n".join(lines) + "\n")
    print(f"PASS: dashboard rendered -> {OUT}")


if __name__ == "__main__":
    main()
