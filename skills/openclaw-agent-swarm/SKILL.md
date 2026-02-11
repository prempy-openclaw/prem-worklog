---
name: openclaw-agent-swarm
description: Build and operate a startup-style AI agent swarm in OpenClaw with role specialization, handoff contracts, model routing, and rollout guardrails.
metadata: {}
---

# OpenClaw Agent Swarm Blueprint

## 1) Recommended Architecture

Use a **Hub-and-Spoke** structure:
- Hub: `coordinator`
- Spokes: `researcher`, `engineer`, `art`, `qa`, `ops`

Layering in OpenClaw:
1. Multi-agent routing for persistent role isolation (workspace/persona/tool policy)
2. `sessions_spawn` subagents for temporary parallel subtasks

## 2) Role Cards

### coordinator
- triage, planning, ownership assignment, final merge
- outputs: task plan, decision log, integrated summary

### researcher
- evidence gathering, benchmarking, requirement clarification
- outputs: brief + sources + confidence

### engineer
- implementation, refactor, testing
- outputs: change summary + verification commands + risks

### art
- design direction, copy, visual prompt specs
- outputs: variants + rationale + asset specification

### qa
- acceptance checks, regressions, edge cases
- outputs: pass/fail report + reproducible bug list

### ops
- automation, cron, monitoring, rollback/runbooks
- outputs: runbook + alerts + rollback procedure

## 3) Handoff Contract

All agents must hand off in a fixed schema:

```yaml
task_id: <id>
owner: <role>
input_summary: <what was received>
output_summary: <what was produced>
artifacts:
  - path/url
verification:
  - command/result
risks:
  - <risk>
next_handoff_to: <role>
status: done|blocked|needs_review
```

Rules:
- no handoff without verification
- blocked tasks must include explicit unblock conditions

## 4) Model Routing by Role

- coordinator: Opus (judgment-heavy)
- researcher: Sonnet (analysis/synthesis)
- engineer: Codex-family (execution-heavy coding loops)
- art: Sonnet (creative + structure)
- qa: Sonnet/Codex based on test depth
- ops: Haiku/Sonnet depending on complexity

## 5) Tool Policy by Role

- coordinator: session orchestration + read
- researcher: browser/web_fetch/read/write
- engineer: exec/process/read/write/edit
- art: browser/read/write
- qa: exec/read/process
- ops: cron/gateway/exec/read

Apply per-agent sandbox and allow/deny lists.

## 6) Failure Modes and Guardrails

Common failures:
1. token burn from uncontrolled fan-out
2. duplicate work from unclear ownership
3. context rot in long threads
4. false completion without verification

Guardrails:
1. cap parallel subagents (2–3 initially)
2. single owner per task
3. mandatory verification before close
4. refresh context when threads bloat
5. run noisy periodic jobs in isolated cron sessions

## 7) 14-Day Rollout

### Week 1
- D1-2: launch 3 agents (coordinator/researcher/engineer)
- D3: enforce handoff contract
- D4: add qa
- D5: run first mini-project end-to-end
- D6-7: measure throughput, quality, cost

### Week 2
- D8: add art + ops
- D9: add daily status cron
- D10: finalize blocked/retry/escalation playbook
- D11-12: run two parallel delivery streams
- D13: tune model routing
- D14: lock SOP v1

## 8) KPIs

- throughput (tasks/day)
- rework rate
- median time-to-done
- cost per completed task
- blocked-task ratio

If throughput does not improve by ~20% after two weeks, simplify to single-agent + selective subagents.
