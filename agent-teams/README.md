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

## P3 Auto Task Intake

```bash
python3 /root/.openclaw/workspace/agent-teams/intake_task.py <task_id> "<title>" [priority]
```

- Auto-assigns initial owner based on title keywords.
- Creates owner lock immediately.

## P3 Coordinator Auto-Triage

```bash
python3 /root/.openclaw/workspace/agent-teams/coordinator_triage.py
```

- Moves `todo` tasks into `in_progress` for active execution.

## P3 Team Dashboard Render

```bash
python3 /root/.openclaw/workspace/agent-teams/render_dashboard.py
```

Output:
- `agent-teams/DASHBOARD.md` (human-readable team board)

## P4 Release Gate

```bash
python3 /root/.openclaw/workspace/agent-teams/release_gate.py <task_id>
```

Pass criteria:
- qa_status == pass
- verification_pass == true
- task not blocked
- no critical defects open

## P4 Escalation Rules

- File: `agent-teams/escalation_rules.yaml`
- Defines rule-based escalations (blocked timeout, reopen loops, critical defects, owner stall)

## P4 PR / Merge Checklist

- File: `agent-teams/pr_checklist.md`
- Use before merge decision for every delivery task

## P5 Task Scoring

```bash
python3 /root/.openclaw/workspace/agent-teams/task_score.py
```

- Calculates priority score per task.
- Sorts queue by highest score first.

## P5 Smart Reroute

```bash
python3 /root/.openclaw/workspace/agent-teams/smart_reroute.py
```

- Reassigns tasks based on rule triggers (e.g., blocked engineer task -> coordinator).

## P5 Incident Mode

```bash
python3 /root/.openclaw/workspace/agent-teams/incident_mode.py on "<reason>"
python3 /root/.openclaw/workspace/agent-teams/incident_mode.py off
python3 /root/.openclaw/workspace/agent-teams/incident_mode.py status
```

- Enables emergency operating mode flag for stricter triage discipline.

