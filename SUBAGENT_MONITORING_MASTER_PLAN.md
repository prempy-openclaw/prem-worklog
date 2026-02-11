Sub-Agent Monitoring Master Plan
Owner: Prem  
Requester: Oscar  
Mode: Plan-first, Native-first (OpenClaw)

## Progress Tracker
- [x] Master requirements/spec consolidated
- [x] State machine spec drafted (`subagent-monitoring/STATE_MACHINE_SPEC.md`)
- [x] Task contract drafted (`subagent-monitoring/TASK_CONTRACT_V1.md`)
- [x] POC evidence index published (`subagent-monitoring/POC_EVIDENCE_INDEX.md`)
- [x] Backend monitoring API extended (task detail + recovery endpoints)
- [x] Queue/dashboard defaults migrated to `subagent-monitoring/` paths
- [ ] Frontend monitor page wiring for recovery actions + task detail view
- [ ] End-to-end staged deploy and production canary verification
1) Executive Summary

This master document consolidates the requirements, implementation strategy, deployment plan, and work breakdown for restoring sub-agent monitoring tools to their original vision while addressing prior failures (false in-progress states, noisy alerts, weak proof). The plan uses OpenClaw's native capabilities first and adds a minimal custom policy layer to achieve deterministic control and truthful observability.

Design Principle:

Use OpenClaw native primitives first (multi-agent, sessions_spawn, cron/heartbeat).

Introduce a thin custom policy layer for stale/recovery/evidence handling.

Enforce proof-based progress (task -> session -> artifact -> verification).

2) Problem Statement

Previous monitoring solutions failed due to:

Conflation of workflow and execution state: Workflow status (e.g., in_progress, done) was misaligned with the actual runtime execution state, leading to false reporting.

Noisy alerts: Alerts were triggered too frequently and did not provide enough actionable insights.

Weak proof of task completion: Tasks marked as complete without verifiable evidence.

To resolve these issues, we need to decouple workflow state from execution state, enforce evidence-based execution, and ensure reliable operations with minimal noise.

3) Objectives

Truthful Status: Separate workflow_state (reflecting task status) from execution_state (reflecting runtime activity).

Verifiable Execution: Introduce timestamped evidence and verification results to guarantee task completion.

Reliable Operations: Detect stale states, enable deterministic recovery, and reduce alert noise.

Native Compatibility: Integrate seamlessly with OpenClaw's session/sub-agent model without overloading it with custom layers.

4) Scope
In Scope

State Model & Contracts: Define the relationship between workflow_state and execution_state.

Runtime Signal Ingestion: Capture activity, tool calls, artifact writes, and errors.

Reconciliation Logic: Map runtime state to task state and detect discrepancies.

Monitoring APIs & Realtime Streams: Expose task states, logs, and recovery actions.

UI & Dashboards: Visualize real-time task execution with truthful state separation.

Alerting & Stale Recovery: Implement intelligent alerting, recovery, and escalation policies.

Deployment & Rollback Plans: Provide a robust deployment and rollback process.

Out of Scope (v1)

Custom Workflow Engine: No replacement of OpenClaw with a custom engine.

Fully Autonomous Orchestration: Avoid fully autonomous orchestration without human oversight.

Enterprise-Grade RBAC: Fine-grained role-based access control will be deferred.

5) Core Architecture (Native-First)
Layer A - OpenClaw Native (Mandatory)

Multi-Agent Role Isolation: Isolate tasks into different agents based on role to avoid overlap and confusion.

Subtask Parallelization: Use sessions_spawn to allow parallel task execution.

Scheduled Checks: Use cron/heartbeat to validate task activity.

Session Traceability: Utilize session-based tracking to ensure full execution proof.

Layer B - Thin Custom Policy (Minimal)

Execution Stale Detection: Implement policies to detect when a task is stale (no activity for a defined period).

Recovery & Escalation: Create policies for task recovery and escalation based on execution states.

Evidence Validation: Ensure all completed tasks have verifiable proof (artifacts and verification results).

Alert Deduplication & Cooldown: Avoid spam by introducing deduplication logic and cooldown between similar alerts.

Layer C - Monitoring UI/API

Summary & Task List: Show current task statuses along with detailed execution logs.

Realtime Stream: Provide a live view of task activity via a streaming API.

Truthful Split: Differentiate between workflow_state (task progress) and execution_state (runtime activity).

6) Canonical Data Definitions
6.1 State Definitions

workflow_state: Represents the task's intended status (e.g., todo, in_progress, done).

execution_state: Represents the actual runtime status (e.g., active, idle, stale, error).

Note: execution_state is derived solely from runtime activity and should never be inferred from workflow_state.

6.2 Required Task Fields

task_id (immutable)

title

owner

priority

workflow_state

execution_state

next_action (required if in_progress)

eta (required if in_progress)

created_at, updated_at, last_action_at (UTC)

evidence_path (required if done)

verification_result (required if done)

6.3 Validation Rules

in_progress requires both next_action and eta.

done requires both evidence_path and verification_result.

Task ownership changes require an explicit handoff reason.

7) Functional Requirements
FR-1 Task Contract & Handoff

Every dispatched task must include:

Objective

Expected artifact path

Verification command

Timeout

Fallback owner

Sub-agent output must include:

Status

Artifact path

Verification result

Risk notes

Next handoff

FR-2 Runtime Signal Ingestion

We will collect:

Session activity

Tool call/result events

Artifact writes

Verification outputs

Timeout/error events

FR-3 Reconciliation Logic

Mapping Rules:

Active: Task is active if there's recent activity (<= 3 minutes).

Idle: Task is idle if no activity for 3 minutes but still within the stale threshold.

Stale: Task is stale if no activity exceeds the stale threshold.

Unknown: Task is unknown if no signals are received.

Error: Task is in error if there's a tool failure or timeout.

FR-4 Monitoring APIs

Required endpoints:

GET /api/v1/monitoring/summary

GET /api/v1/monitoring/tasks

GET /api/v1/monitoring/task/:task_id

GET /api/v1/monitoring/logs?agent=<id>&limit=50

GET /api/v1/monitoring/stream (SSE)

POST /api/v1/monitoring/recovery/reassign

POST /api/v1/monitoring/recovery/escalate

FR-5 Dashboard UX

Mandatory views:

Global summary strip

Task table with both states

Per-agent realtime panel

CLI-like logs (50-row cap + fullscreen)

Evidence panel (artifact + verification)

Stale/alert panel

FR-6 Alerting

Alerting will be triggered on significant transitions:

Idle → Stale

Stale → Escalated

Error states

Alert deduplication and cooldown (15 minutes) will apply to reduce noise.

FR-7 Recovery Workflow

Thresholds:

Warning: 10 minutes without activity

Stale: 20 minutes without activity

Escalation: 30 minutes without activity

Recovery actions:

Reassign at stale state

Escalate after threshold

Audit logs for all recovery actions

8) Non-Functional Requirements

Truthfulness: No fake active statuses; all states must be runtime-derived.

Performance: Summary queries should have a p95 response time of < 300ms, logs queries should be < 400ms.

Reliability: Degraded sources should return an unknown state, with no system crashes.

Maintainability: Reconciliation logic should be centralized and unit-tested.

Observability: An audit trail must exist for all alert and recovery decisions.

9) Acceptance Criteria (Must Pass)

Invalid in_progress (missing next_action or eta) is rejected.

No-activity tasks transition to stale when the threshold is exceeded.

Alerts with cooldown prevent repeated spam.

The UI should clearly show discrepancies between workflow_state and execution_state.

Logs panel supports 50-row cap with fullscreen mode.

Evidence chain (task → event → artifact → verify) must be navigable.

All recovery actions (reassign/escalate) must be logged.

Parallel POCs (>=3 tasks) must generate timestamped evidence.

10) Deployment Plan
DEP-1 Build & Package

Run tests/lint/build for each service.

Build the container image and tag it as <service>:<git-sha>.

Gate: All checks must pass.

DEP-2 Staging Deploy

Deploy one service at a time and perform smoke checks on routing paths (/, /money, /monitor) and monitoring APIs.

DEP-3 Progressive Production Rollout

Rollout order: agent-monitor → home-shell → money-manager.
Canary testing (10% → 50% → 100%) with monitoring for error rates and stale mismatches.

DEP-4 Post-Deploy Verification

Validate execution state truthfulness.

Validate alert deduplication and cooldown behavior.

Validate logs/fullscreen functionality.

Validate proof chain views.

DEP-5 Operational Guardrails

Critical alerts only.

Noisy alerts off by default.

Emergency global alerts-off switch.

11) Work Breakdown & Ownership Plan
WS-A Architecture & Contracts (Coordinator)

A1: Finalize state schema.

A2: Define task contracts and handoff policies.

A3: Establish acceptance policies.

Deliverables: STATE_MACHINE_SPEC.md, TASK_CONTRACT_V1.md

WS-B Backend Monitoring Core (Engineer)

B1: Implement signal collector.

B2: Implement reconciliation engine.

B3: Create monitoring APIs.

B4: Implement alert deduplication and cooldown.

B5: Implement recovery endpoints.

Deliverables: Monitoring API implementation, reconciliation tests.

WS-C Dashboard UX (Engineer + QA)

C1: Implement workflow/execution split views.

C2: Display stale + last_action visibility.

C3: Implement CLI-like logs + fullscreen.

C4: Display evidence/proof panels.

Deliverables: UI updates, UX checklist.

WS-D Validation & Proof (QA)

D1: Execute acceptance suite.

D2: Simulate stale/recovery scenarios.

D3: Run parallel POC evidence pack.

Deliverables: ACCEPTANCE_REPORT.md, POC_EVIDENCE_INDEX.md.

WS-E DevOps & Release (Ops/Coordinator)

E1: Set up independent CI pipelines.

E2: Implement deploy pipelines.

E3: Create routing + rollback scripts.

E4: Write operational runbooks.

Deliverables: CI/CD workflows, DEPLOY_RUNBOOK.md, ROLLBACK_RUNBOOK.md.

12) Milestones

M1: Foundation (WS-A + WS-B1/B2)

M2: Visibility (WS-B3 + WS-C1/C2)

M3: Control (WS-B4/B5 + WS-C3/C4 + WS-E1/E2)

M4: Proof & Signoff (WS-D + WS-E3/E4)

13) Risk Register

False Active Status: Ensure execution state is derived only from runtime data.

Token Burn & Fan-Out: Limit concurrent sub-agent activity to prevent overload.

Alert Noise: Implement deduplication, cooldown, and severity filters.

Weak Closure Quality: Enforce mandatory evidence and verification gates.

14) Exit Criteria (Production Ready)

The system is considered restored when:

Dashboard status accurately reflects task progress.

Parallel sub-agent execution is verifiably proven with timestamped evidence.

Alerts are high-signal, low-noise.

Completed tasks have a complete proof chain.

15) Next Immediate Actions

Generate STATE_MACHINE_SPEC.md.

Generate TASK_CONTRACT_V1.md.

Implement skeleton for WS-B1/B2 and run initial tests.

Publish POC_EVIDENCE_INDEX.md after running POC suite.
