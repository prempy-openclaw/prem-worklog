# Plan Mode — OpenClaw Native Multi-Agent Development Plan

Owner: Prem  
Mode: Plan-first (no broad automation rollout until checkpoints pass)

## 1) Objective
Rebuild agent teamwork using **OpenClaw native primitives first**:
- Multi-agent routing (isolated roles)
- `sessions_spawn` for parallel sub-work
- Cron/heartbeat only as scheduler (not fake executor)

And add only a **thin custom policy layer** for SLA/stale handling.

---

## 2) Success Criteria (Definition of Done)
1. Team state is truthful: `workflow_state` and `execution_state` cannot conflict silently.
2. Parallel work is observable with timestamps and artifact proof.
3. No noisy spam loops from automation.
4. Every in-progress task has owner + ETA + next_action.
5. Recovery path exists: stale -> reassign/escalate in deterministic steps.

---

## 3) Scope
### In Scope
- Native multi-agent config design
- Role/tool/model policy
- Spawn pattern for real parallelization
- Runtime monitoring signals (heartbeat/action/stale)
- Operational runbook

### Out of Scope (for v1)
- Heavy custom workflow engine
- Complex queue orchestration replacing OpenClaw session model
- Full autonomous always-on system without guardrails

---

## 4) Architecture Principle (Native-First)
### Layer A — OpenClaw Native (mandatory)
- Agents: `coordinator`, `researcher`, `engineer`, `qa` (optional `ops`, `art`)
- Routing and isolation by agent/workspace
- Parallel execution via `sessions_spawn`
- Scheduled checks via cron (isolated jobs)

### Layer B — Thin Policy Layer (minimal custom)
- Stale detection policy
- Escalation rule table
- Evidence formatter (timestamps + artifact links)

No thick custom dispatcher until v1 metrics prove need.

---

## 5) Phased Plan (Plan Mode)
## Phase 0 — Baseline & Reset
- Remove old noisy team automations and stale rules.
- Define clean baseline metrics:
  - time-to-first-action
  - task completion lead time
  - stale ratio
- Output: baseline snapshot document.

## Phase 1 — Native Team Re-Enable
- Enable only core agents and bindings.
- Apply role cards + tool allow/deny.
- Set OpenAI-only model routing by role.
- Output: `TEAM_CONFIG_V1.md` + verified config.

## Phase 2 — Parallel Execution Pattern
- Standardize spawn contracts:
  - task objective
  - expected artifact
  - timeout
  - handoff schema
- Cap concurrent subagents (start 2–3).
- Output: `PARALLEL_EXECUTION_PLAYBOOK.md`.

## Phase 3 — Truthful Monitoring
- Dashboard must show both:
  - `workflow_state` (task board)
  - `execution_state` (active/idle/unknown + last_action_at)
- Add proof-of-work panel:
  - last action timestamp
  - latest artifact path
  - latest verification command result
- Output: monitor acceptance checklist.

## Phase 4 — Guardrails & Recovery
- Stale policy:
  - warning threshold
  - reroute threshold
  - escalation threshold
- Alert dedupe and cooldown windows.
- Output: `RECOVERY_POLICY_V1.md`.

## Phase 5 — Controlled Automation
- Re-enable only required cron jobs with strict filters.
- Keep high-noise jobs disabled by default.
- Add rollback switch for all team alerts.
- Output: `AUTOMATION_RUNBOOK_V1.md`.

---

## 6) Role Policy (v1)
- **coordinator**: orchestration, acceptance merge, escalation
- **researcher**: source-backed findings only
- **engineer**: implementation + verification commands
- **qa**: acceptance gate + regression checks
- optional **ops**: cron/runbook/rollback

Rules:
- One task, one owner at a time.
- No done without verification evidence.
- Inter-agent communication in English.

---

## 7) KPI Targets (2-week pilot)
- Throughput +20%
- Stale in-progress ratio < 10%
- Rework rate < 15%
- Mean time to first action < 5 min (when triggered)
- Alert noise < 2 false alerts/day

If targets fail, simplify to single-agent + selective subagents.

---

## 8) Risks & Mitigations
1. **Fake activity / stale state drift**
   - Mitigation: execution_state from real session activity, not task text.
2. **Token burn from fan-out**
   - Mitigation: hard cap subagent concurrency and timeout defaults.
3. **Alert spam**
   - Mitigation: dedupe + cooldown + severity tiers.
4. **Completion without evidence**
   - Mitigation: strict verification gate before done.

---

## 9) Immediate Next Actions
1. Draft `TEAM_CONFIG_V1.md` from current OpenClaw config.
2. Implement `PARALLEL_EXECUTION_PLAYBOOK.md` template.
3. Add truthful monitor acceptance tests.
4. Re-enable only essential cron jobs after validation.

---

## 10) Decision Log
- Native-first over custom-heavy orchestration.
- Plan mode enforced before full autonomous rollout.
- Execution proof required for progress claims.
