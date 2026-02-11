---
name: claude-vs-codex-selection
description: Practical guide to choose between Claude Opus 4.6 and GPT-5.x Codex for coding and agent tasks, based on official docs and cost/performance tradeoffs.
metadata: {}
---

# Claude Opus 4.6 vs GPT-5.x Codex — Model Selection Skill

ใช้ skill นี้เมื่ออยากเลือก model ให้เหมาะกับงาน coding/agentic workflows ระหว่าง Claude และ GPT Codex

## Evidence Sources (เชื่อถือได้)

- Anthropic Models Overview: https://platform.claude.com/docs/en/about-claude/models/overview
- Anthropic Pricing: https://platform.claude.com/docs/en/about-claude/pricing
- OpenAI Models index: https://developers.openai.com/api/docs/models
- OpenAI GPT-5-Codex page: https://developers.openai.com/api/docs/models/gpt-5-codex
- OpenAI Latest model guide (GPT-5.2 family): https://developers.openai.com/api/docs/guides/latest-model

> Note: OpenAI public docs currently document **GPT-5-Codex / GPT-5.2-Codex** clearly. If runtime shows `gpt-5.3-codex`, treat it as a newer codex-family variant and validate behavior in your workload.

---

## Quick Comparison (practical)

| Dimension | Claude Opus 4.6 | GPT-5.x Codex |
|---|---|---|
| Positioning | Most intelligent Claude model for complex coding/reasoning | Codex-optimized GPT model for agentic coding workflows |
| Reasoning profile | Strong deep reasoning, long multi-step analysis | Strong coding execution/orchestration in Codex-like envs |
| Context window | 200K (1M beta) | 400K (from GPT-5-Codex docs) |
| Max output | 128K | 128K |
| Tooling orientation | Excellent with agent/tool loops | Explicitly optimized for Codex agentic coding |
| Price (input/output per MTok) | $5 / $25 | $1.25 / $10 (GPT-5-Codex docs) |
| Cost posture | Premium quality | Much cheaper for high-volume coding loops |

---

## Selection Rules (ใช้งานจริง)

### เลือก **Claude Opus 4.6** เมื่อ:

1. งานเป็น **hard reasoning** หรือ architecture ที่ ambiguity สูง
2. ต้องการคุณภาพการอธิบาย/สรุป/decision memo ระดับสูง
3. งานเกี่ยวกับ multi-domain analysis (tech + product + tradeoff)
4. ต้องการผลลัพธ์แม่นยำมากกว่า speed/cost

**Examples**
- ออกแบบระบบ payment + idempotency + failure recovery
- วาง migration plan monolith → microservices แบบมี rollback strategy
- วิเคราะห์ root cause incident ซับซ้อนจากหลาย log source

### เลือก **GPT-5.x Codex** เมื่อ:

1. งานเป็น **coding execution loop** ชัดเจน (implement → test → fix)
2. ต้องการ throughput สูงและควบคุม cost
3. งาน agentic coding ระยะยาวใน Codex-like environment
4. งานต้อง iterate เยอะ (หลายไฟล์ หลายรอบ)

**Examples**
- เขียน/แก้ test จำนวนมาก
- ทำ repetitive refactor ตาม pattern
- runbook automation + tooling integration

---

## Hybrid Strategy (แนะนำที่สุด)

ใช้สองตัวร่วมกัน:

1. **Opus 4.6 for planning**
   - ให้ model ออกแบบแผน, risk, acceptance criteria
2. **GPT-5.x Codex for execution**
   - ลงมือแก้โค้ดรอบใหญ่ๆ และ iterate เร็ว
3. **Opus 4.6 for final review**
   - ตรวจคุณภาพสุดท้าย, security/edge cases, design integrity

สูตรนี้มักได้ทั้งคุณภาพและต้นทุนที่ดี

---

## Cost-first Routing Template

- Small/simple coding task → GPT-5.x Codex
- Medium feature implementation → GPT-5.x Codex
- Complex architecture or critical bug RCA → Claude Opus 4.6
- Final high-stakes review before merge/release → Claude Opus 4.6

---

## OpenClaw Usage Pattern

### For user-facing main chat
- Default to model that user prefers for quality (often Opus)

### For sub-agents / cron / bulk jobs
- Use cheaper coding model (GPT-5.x Codex) for repetitive implementation
- Escalate to Opus only when quality/risk threshold requires

---

## Verification Checklist

ก่อน lock-in model ให้ลอง A/B 3 งานจริงของตัวเอง:

1. งานยาก (architecture/debug)
2. งานกลาง (feature)
3. งานง่ายแต่เยอะ (bulk edits/tests)

วัด 4 metric:
- correctness
- time to done
- total token cost
- rework needed after output

แล้วค่อยตั้ง policy ถาวร

---

## Default Recommendation (if unsure)

- เริ่มที่ **GPT-5.x Codex** สำหรับ coding execution
- ถ้างานเริ่มตัน/คุณภาพไม่พอ/decision ซับซ้อน → switch เป็น **Claude Opus 4.6**

"Codex for momentum, Opus for judgment."