# SUBAGENT MONITORING MASTER PLAN

Owner: Prem  
Requester: Oscar  
Mode: Plan-first, Native-first (OpenClaw)

---

## 1) Executive Summary
This master document consolidates requirements, implementation strategy, deployment strategy, and work breakdown for restoring **sub-agent monitoring tools** to the original vision—while fixing prior failures (false in-progress states, noisy alerts, weak proof).

Design principle:
1. Use OpenClaw native primitives first (`multi-agent`, `sessions_spawn`, `cron/heartbeat`)  
2. Add only a thin custom policy layer (stale/recovery/evidence)  
3. Enforce proof-based progress (task -> session -> artifact -> verification)

---

## 2) Problem Statement
Previous setup degraded because:
- Workflow state and runtime execution were conflated.
- Tasks looked active without real agent activity.
- Alerts were noisy and repetitive.
- Completion was possible without hard evidence.

We need truthful runtime observability and deterministic control.

---

## 3) Objectives
1. Truthful status: separate `workflow_state` and `execution_state`.
2. Verifiable execution: timestamped evidence and verification results.
3. Reliable operations: stale detection, deterministic recovery, low-noise alerting.
4. Native compatibility: fit OpenClaw session/sub-agent model without heavy custom engine.

---

## 4) Scope
### In Scope
- State model and contracts
- Runtime signal ingestion
- Reconciliation logic
- Monitoring APIs + realtime stream
- Dashboard views and logs
- Alerting + stale recovery
- Deployment and rollback plan
- Work breakdown with ownership

### Out of Scope (v1)
- Replacing OpenClaw with a custom workflow engine
- Fully autonomous no-guardrail orchestration
- Enterprise RBAC fine-grain model

---

## 5) Core Architecture (Native-First)

## Layer A — OpenClaw Native (Mandatory)
- Multi-agent role isolation
- Subtask parallelization via `sessions_spawn`
- Scheduled checks via cron/heartbeat
- Session-based traceability for execution proof

## Layer B — Thin Custom Policy (Minimal)
- Execution stale detection
- Recovery/escalation policies
- Evidence validator and proof chain formatter
- Alert dedupe/cooldown

## Layer C — Monitoring UI/API
- Summary + task list + detailed logs
- Realtime stream
- Truthful split of workflow vs execution

---

## 6) Canonical Data Definitions

### 6.1 State Definitions
- `workflow_state`: `todo | in_progress | waiting | review | done | blocked`
- `execution_state`: `active | idle | unknown | stale | error`

Rule: execution state is derived only from runtime activity, never from workflow labels.

### 6.2 Required Task Fields
- `task_id` (immutable)
- `title`
- `owner`
- `priority`
- `workflow_state`
- `execution_state`
- `next_action` (required if in_progress)
- `eta` (required if in_progress)
- `created_at`, `updated_at`, `last_action_at` (UTC)
- `evidence_path` (required if done)
- `verification_result` (required if done)

### 6.3 Validation Rules
1. `in_progress` requires `next_action` + `eta`
2. `done` requires evidence + verification pass
3. Owner change requires handoff reason

---

## 7) Functional Requirements

## FR-1 Task Contract & Handoff
Every dispatched task must include:
- objective
- expected artifact path
- verification command
- timeout
- fallback owner

Sub-agent output must include:
- status
- artifact_path
- verification
- risk_notes
- next_handoff

## FR-2 Runtime Signal Ingestion
Collect:
- session activity
- tool call/result events
- artifact writes
- verification command outputs
- timeout/error events

## FR-3 Reconciliation Logic
Default mapping:
- activity <= 3m -> `active`
- activity > 3m and <= stale threshold -> `idle`
- no activity > stale threshold -> `stale`
- no source -> `unknown`
- runtime/tool failure -> `error`

Conflict visibility rule:
If `workflow_state=in_progress` and `execution_state!=active`, show explicit mismatch badge.

## FR-4 Monitoring APIs
Required endpoints:
- `GET /api/v1/monitoring/summary`
- `GET /api/v1/monitoring/tasks`
- `GET /api/v1/monitoring/task/:task_id`
- `GET /api/v1/monitoring/logs?agent=<id>&limit=50`
- `GET /api/v1/monitoring/stream` (SSE)
- `POST /api/v1/monitoring/recovery/reassign`
- `POST /api/v1/monitoring/recovery/escalate`

## FR-5 Dashboard UX
Mandatory views:
- global summary strip
- task table with both states
- per-agent realtime panel
- CLI-like logs (50 row cap + fullscreen)
- evidence panel (artifact + verification)
- stale/alert panel

## FR-6 Alerting
- Trigger only on major transitions (`idle->stale`, `stale->escalated`, `error`)
- Apply cooldown (default 15m)
- Deduplicate repeated alerts per task

## FR-7 Recovery Workflow
Thresholds:
- warning: 10m no activity
- stale: 20m
- escalate: 30m

Recovery actions:
- suggest reassign at stale
- escalate by severity after threshold
- write audit log for all recovery actions

---

## 8) Non-Functional Requirements
- Truthfulness: no fake active status
- Performance: summary p95 < 300ms, log query p95 < 400ms
- Reliability: degraded sources -> `unknown`, no hard crash
- Maintainability: reconciliation centralized and unit-tested
- Observability: audit trail for alert/recovery decisions

---

## 9) Acceptance Criteria (Must Pass)
1. Invalid `in_progress` (missing next_action/eta) is rejected
2. No-activity tasks cross to stale at threshold
3. Cooldown prevents duplicate alert spam
4. UI clearly shows workflow/execution mismatch
5. Logs panel supports 50-row cap + fullscreen
6. Evidence chain is navigable task->event->artifact->verify
7. Reassign/escalation actions are audited
8. Parallel POC (>=3 tasks) produces timestamped evidence

---

## 10) Deployment Plan

## DEP-0 Preconditions
- Service split is available: `home-shell`, `money-manager`, `agent-monitor`
- Env vars and routing basenames configured (`/`, `/money`, `/monitor`)
- Monitoring paths configured and readable

## DEP-1 Build & Package
Per service:
1. run tests/lint/build
2. build container image
3. tag as `<service>:<git-sha>`

Gate: all checks pass.

## DEP-2 Staging Deploy (Independent)
Deploy one service at a time.
Smoke check:
- `/`
- `/money/`
- `/monitor/`
- monitoring APIs

Gate: all endpoints healthy; no routing regressions.

## DEP-3 Progressive Production Rollout
Order:
1. `agent-monitor`
2. `home-shell`
3. `money-manager` (only if changed)

Rollout mode:
- 10% canary -> 50% -> 100%
- verify error rate, latency, stale mismatch before promotion

Rollback:
- revert only impacted service image tag
- no cross-service rollback unless shared infra issue

## DEP-4 Post-Deploy Verification
- validate execution-state truthfulness
- validate alert dedupe/cooldown
- validate logs/fullscreen behavior
- validate proof chain view

## DEP-5 Operational Guardrails
- noisy alerts off by default
- critical transitions only
- emergency global alerts-off switch

---

## 11) Work Breakdown & Ownership Plan

## WS-A Architecture & Contracts (Coordinator)
- A1 state schema finalization
- A2 handoff/task contracts
- A3 acceptance policy

Deliverables:
- `STATE_MACHINE_SPEC.md`
- `TASK_CONTRACT_V1.md`

## WS-B Backend Monitoring Core (Engineer)
- B1 signal collector
- B2 reconciliation engine
- B3 monitoring APIs
- B4 alert dedupe/cooldown
- B5 recovery endpoints

Deliverables:
- monitoring API implementation
- reconciliation tests

## WS-C Dashboard UX (Engineer + QA)
- C1 workflow/execution split views
- C2 stale + last_action visibility
- C3 CLI-like logs + fullscreen
- C4 evidence/proof panels

Deliverables:
- UI updates + UX checklist

## WS-D Validation & Proof (QA)
- D1 acceptance suite execution
- D2 stale/recovery simulation
- D3 parallel POC evidence pack

Deliverables:
- `ACCEPTANCE_REPORT.md`
- `POC_EVIDENCE_INDEX.md`

## WS-E DevOps & Release (Ops/Coordinator)
- E1 independent CI pipelines per repo
- E2 independent deploy pipelines
- E3 routing + rollback scripts
- E4 operational runbooks

Deliverables:
- CI/CD workflows
- `DEPLOY_RUNBOOK.md`
- `ROLLBACK_RUNBOOK.md`

---

## 12) Milestones (No Day-Based Timeline)
- **M1 Foundation**: WS-A + WS-B1/B2
- **M2 Visibility**: WS-B3 + WS-C1/C2
- **M3 Control**: WS-B4/B5 + WS-C3/C4 + WS-E1/E2
- **M4 Proof & Signoff**: WS-D + WS-E3/E4

---

## 13) Risk Register
1. False active status -> enforce runtime-derived execution only
2. Token burn fan-out -> cap concurrent sub-agents + timeout
3. Alert noise -> dedupe + cooldown + severity filtering
4. Weak closure quality -> mandatory evidence and verification gate

---

## 14) Exit Criteria (Production Ready)
System is considered restored when:
1. dashboard status is truthful
2. parallel sub-agent execution is reproducibly proven
3. alerts are high-signal, low-noise
4. each completed task has full proof chain

---

## 15) Next Immediate Actions
1. Generate `STATE_MACHINE_SPEC.md`
2. Generate `TASK_CONTRACT_V1.md`
3. Implement WS-B1/B2 skeleton and tests
4. Run POC suite and publish `POC_EVIDENCE_INDEX.md`
