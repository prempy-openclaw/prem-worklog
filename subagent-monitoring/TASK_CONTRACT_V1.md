# TASK_CONTRACT_V1

## Dispatch Input (Coordinator -> Sub-agent)
```yaml
task_id: TASK-YYYYMMDD-XXX
owner: engineer|researcher|qa|ops|art
objective: string
expected_artifact_path: /absolute/or/workspace/path
verification_command: string
timeout_seconds: number
fallback_owner: coordinator|qa|ops
priority: low|medium|high|critical
next_action: string
eta: string
```

## Sub-agent Output Contract
```yaml
task_id: TASK-YYYYMMDD-XXX
status: done|blocked|needs_review
artifact_path: path
verification:
  command: string
  result: pass|fail
risk_notes:
  - string
next_handoff: coordinator|qa|engineer|ops
updated_at: UTC_ISO8601
```

## Validation Checklist
- status=done -> verification.result=pass + artifact_path exists
- status=blocked -> must include unblock conditions in risk_notes
- all timestamps UTC
- communication between agents in English only
