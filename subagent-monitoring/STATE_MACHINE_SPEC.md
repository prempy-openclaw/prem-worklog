# STATE_MACHINE_SPEC

## Workflow State
- `todo` -> `in_progress` -> `review` -> `done`
- `todo` -> `blocked`
- `in_progress` -> `waiting` -> `in_progress`
- `in_progress|review|waiting` -> `blocked`
- `blocked` -> `in_progress|waiting`

Hard rules:
- `in_progress` requires `next_action` and `eta`
- `done` requires `evidence_path` and `verification_result=pass`
- owner change requires recovery/handoff reason

## Execution State (runtime-derived)
- `active`: last owner activity <= 3 minutes
- `idle`: no activity > 3 minutes and <= stale threshold
- `stale`: no activity > stale threshold
- `unknown`: no signal source available
- `error`: task blocked/runtime failure

## Conflict Visibility
If `workflow_state=in_progress` and `execution_state!=active`, dashboard must show mismatch badge:
`In-progress (not executing)`

## Threshold Defaults
- warning: 10m
- stale: 20m
- escalate: 30m
