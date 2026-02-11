# Agent Monitoring Dashboard — UI Spec Pack v1

## 1) Screen Map
1. **Overview (God View)**
   - Live topology graph (agent ↔ agent / agent ↔ tool)
   - Global KPI strip (active agents, in-progress tasks, blocked, error rate, p95 latency, cost today)
   - Queue bottleneck panel
2. **Agents**
   - Agent cards: status, current task, last heartbeat, token/cost, latency
   - Drill-in to agent timeline
3. **Tasks**
   - Backlog/In-progress/Done/Blocked board
   - Task detail: owner, handoffs, verification, release gate status
4. **Trace Explorer**
   - Full conversation thread timeline
   - Step-by-step event playback
   - Tool call/output inspection
5. **Safety & Control**
   - Circuit breaker states and incidents
   - Approval gate queue
   - Takeover mode (human override)
6. **Cost & Performance**
   - Token/cost by agent, by task, by day
   - Latency breakdown: model/tool/db/network

## 2) Core Components
- `TopologyGraph`
- `GlobalStateViewer`
- `QueueHeatmap`
- `AgentStatusCard`
- `TaskBoard`
- `TraceTimeline`
- `ReplayController`
- `CircuitBreakerPanel`
- `ApprovalGateQueue`
- `TakeoverConsole`
- `CostTrendChart`
- `LatencyBreakdownChart`

## 3) UX Behavior
- **Color semantics**
  - 🟢 healthy/idle
  - 🟡 running/thinking
  - 🟠 degraded/warning
  - 🔴 error/blocked
- **Realtime**
  - WebSocket primary, SSE fallback
  - Reconnect with backoff + stale data banner
- **Critical alerts**
  - Sticky top banner for blocked critical tasks or tripped circuit breakers
- **Trace drill-down**
  - Max 3 clicks from dashboard to failing span/tool output

## 4) Design Tokens (v1)
- **Typography**: Inter (UI), JetBrains Mono (logs)
- **Spacing scale**: 4, 8, 12, 16, 24, 32
- **Radius**: 10 (cards), 8 (inputs/buttons)
- **Elevation**: light shadow only for active/focused panels
- **Theme**: dark-first ops theme
  - BG: #0B1020
  - Surface: #121A2B
  - Primary: #4F8CFF
  - Success: #18C37E
  - Warning: #F5B93B
  - Danger: #F05D5E
  - Text: #E6ECFF / #9FB0D9

## 5) Wireframe Notes (text)
- **Overview layout**
  - Row 1: KPI strip (6 cards)
  - Row 2: Left 8/12 = TopologyGraph, Right 4/12 = Alerts + Circuit status
  - Row 3: Left 6/12 = QueueHeatmap, Right 6/12 = GlobalStateViewer
- **Trace Explorer**
  - Left: timeline list
  - Center: span tree
  - Right: payload/tool output JSON panel
- **Safety & Control**
  - Tabs: Approvals / Breakers / Takeover / Audit Log

## 6) MVP vs V2 (UI)
### MVP
- Overview, Agents, Tasks, Trace Explorer
- Basic Safety panel (breaker + approvals)
- Cost/Latency charts (daily + per-agent)

### V2
- Replay diff visualizer (original vs replay)
- Predictive bottleneck warnings
- Policy editor with simulation mode
- Team comparison dashboard

## 7) Handoff Notes for Frontend Build
- Start with reusable data model for `agent_state`, `task`, `event`, `trace_span`.
- Build pages in this order: Overview → Tasks → Trace Explorer → Safety.
- Add role-based visibility from day 1 (viewer/operator/admin).
