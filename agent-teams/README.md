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
