# ROLLBACK_RUNBOOK

## Trigger conditions
- monitoring APIs failing
- false active flood
- alert storm
- severe UI regression in `/monitor`

## Rollback steps
1. Revert only impacted service image tag.
2. Keep other services untouched.
3. Verify:
   - `/api/v1/monitoring/summary`
   - `/api/v1/monitoring/tasks`
4. If alert storm: set alerts-off switch in ops config.

## Data safety
- Do not delete `task_queue.yaml` during rollback.
- Preserve evidence docs and artifact files.

## Exit rollback
- root cause identified
- fixed image validated in staging
- redeploy with canary again
