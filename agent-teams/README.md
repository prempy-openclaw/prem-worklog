# Agent Team Operating Rules (P0)

## Mandatory Handoff Contract

Every role must return output using `HANDOFF_TEMPLATE.yaml` fields.
If `verification` is missing, the task is not considered complete.

## QA Gate (Hard Rule)

Engineer cannot mark implementation as final `done` until:
1. QA status is `done`, or
2. Coordinator grants explicit waiver with reason.

## Owner Lock

Each task has one owner role at a time. Re-assignment must be explicit in handoff.

## Blocked Escalation (SLA)

If `status=blocked`, include exact unblock condition and hand off to coordinator.

SLA:
- blocked for >15 minutes -> escalate to coordinator immediately
- coordinator must decide: unblock path, reassign owner, or explicit waiver

## Contract Validator

Use this script before closing tasks:

```bash
python3 /root/.openclaw/workspace/agent-teams/validate_handoff.py <handoff.yaml>
```

Close policy:
- `FAIL` => task cannot be closed
- `PASS` + QA gate satisfied => close allowed

## P1 Owner Lock + Queue

Task queue file:

```bash
/root/.openclaw/workspace/agent-teams/task_queue.yaml
```

Claim task (owner lock):

```bash
python3 /root/.openclaw/workspace/agent-teams/claim_task.py <task_id> <owner>
```

Rule:
- If a task is locked by another owner, claim fails.
- Reassignment must be explicit via coordinator decision.

## P1 Daily Standup Generator

Generate standup summary:

```bash
python3 /root/.openclaw/workspace/agent-teams/standup_report.py
```

## P2 Metrics Dashboard (CLI)

```bash
python3 /root/.openclaw/workspace/agent-teams/metrics_report.py
```

Tracks:
- total tasks
- blocked ratio
- rework rate
- median time-to-done

## P2 Blocked Auto-Escalation

```bash
python3 /root/.openclaw/workspace/agent-teams/escalate_blocked.py
```

Rule:
- blocked task older than 15 minutes => mark escalated + include in escalation report

## P2 Weekly Velocity

```bash
python3 /root/.openclaw/workspace/agent-teams/weekly_velocity.py
```

Tracks completed tasks in the last 7 days by owner.
