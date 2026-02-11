# DEPLOY_RUNBOOK

## Strategy
- Independent deploy per service.
- Promote with canary: 10% -> 50% -> 100%.
- Validate monitor truthfulness before full rollout.

## Preflight
1. Build image for changed service.
2. Confirm queue/dashboard paths:
   - `/root/.openclaw/workspace/subagent-monitoring/task_queue.yaml`
   - `/root/.openclaw/workspace/subagent-monitoring/DASHBOARD.md`
   - `/root/.openclaw/workspace/subagent-monitoring/incident_mode.yaml`
3. Confirm monitoring env thresholds.

## Staging Checks
- `GET /api/v1/monitoring/summary`
- `GET /api/v1/monitoring/tasks`
- `GET /api/v1/monitoring/task/:taskId`
- `GET /api/v1/monitoring/logs?agent=coordinator&limit=50`
- `GET /api/v1/monitoring/stream`

## Production Promotion Gate
- error rate stable
- no route regressions
- stale-state detection works
- alerts not spamming (cooldown respected)

## Post-Deploy
- run POC proof suite
- update `ACCEPTANCE_REPORT.md`
