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

## Blocked Escalation

If `status=blocked`, include exact unblock condition and hand off to coordinator.
