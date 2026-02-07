# MEMORY.md - Long-term Memory

## Oscar (User)
- Developer, ambitious, ไม่ยอมแพ้
- Backend focus: Spring Boot, Go, Docker
- Timezone: Asia/Bangkok
- Email: golfpopmei14@gmail.com
- Bank: KBank account suffix 5427

---

## Money Manager Project

### Quick Reference
- **Webhook URL:** `POST https://76.13.182.44.nip.io/api/v1/webhook` (no auth)
- **Dashboard:** https://76.13.182.44.nip.io/app/ (admin/admin123)
- **Project:** `/root/webhook-server/`
- **PostgreSQL:** 76.13.182.44:5432, webhook_db, webhook_user

### K+ SMS Format (Oscar's bank notifications)
```
K PLUS|รายการเงินเข้า|บัญชี xxx-x-x5427-x จำนวนเงิน XX.XX บาท วันที่ D เดือน YY HH:MM น.
K PLUS|รายการโอน/ถอน|บัญชี xxx-x-x5427-x จำนวนเงิน XX.XX บาท วันที่ D เดือน YY HH:MM น.
```

### Account Mapping
- Account ID 1: KBank (Oscar's main, suffix 5427)
- Account ID 2: SCB
- Account ID 3: เงินสด
- Account ID 4: TrueMoney

### AI Agent Workflow
1. `GET /api/v1/webhooks/pending` - Poll pending
2. Parse K+ text (เงินเข้า=INCOME, โอน/ถอน=EXPENSE)
3. `POST /api/v1/transactions` - Create transaction
4. `PATCH /api/v1/webhooks/:id/status` - Mark PROCESSED

---

## Skills & Integrations

### Google Workspace (gog)
- Script: `/root/.openclaw/workspace/skills/gog/gog_helper.py`
- Calendar ID: golfpopmei14@gmail.com

### Notion
- Database ID: 1fbf82d039f880b19182cdb5ac44f31e (no dashes)
- Script: `/root/.openclaw/workspace/skills/notion-skill/notion_helper.py`
- Command: `todo [max_items]` - shows only "Next Up" and "In Progress"
- Status filter: "Next Up", "In Progress" only

### Claude Code
- Version: 2.1.34
- Use for coding tasks when requested

---

## Lessons Learned

1. **Go NULL handling**: Use COALESCE() in SQL or *string in structs
2. **Docker nginx**: Restart nginx after container rebuilds (IPs change)
3. **Thai dates**: ก.พ.=Feb, 69=2569 พ.ศ.=2026 ค.ศ.
4. **Frontend emoji**: Don't display Icon if Name already contains emoji

---

## Cron Jobs Active

| Job | เวลา (ไทย) | ทำอะไร |
|-----|------------|--------|
| Morning Briefing | 07:00 | Calendar + Notion Todo → Discord |
| Webhook Processor | 20:00 | Process pending webhooks (silent) |
| Transaction Summary | 21:00 | สรุป + ถาม category → Discord |

### 9PM Workflow:
1. ดึง pending webhooks
2. แสดง parsed data ให้ Oscar
3. ถาม: "หมวดหมู่อะไร? Note?"
4. Oscar ตอบ เช่น "1: อาหาร" หรือ "ข้าวเย็น"
5. Prem สร้าง transaction + mark PROCESSED
