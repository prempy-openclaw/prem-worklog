# MEMORY.md - Long-term Memory

## Oscar (User)
- Developer, ambitious, ไม่ยอมแพ้
- Backend focus: Spring Boot, Go, Docker
- Timezone: Asia/Bangkok
- Email: golfpopmei14@gmail.com
- Bank: KBank account suffix 5427
- **เป้าหมายหลัก: เข้า Agoda** 🎯
  - HackerRank Practice (coding challenges)
  - English Listening (ฝึกฟัง)
  - Interview Practice (behavioral + technical)
  - เสนอแผน Agoda ทุกครั้งที่มีเวลาว่างและไม่มี deadline เร่งด่วน

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

## Morning Briefing Format (กฎเหล็ก)

Format นี้ต้องใช้ทุกครั้ง ห้ามเปลี่ยน:

1. **✅ Tasks Cleared** — สรุป task ที่ clear ไปเมื่อวานและวันนี้ (ดูจาก Notion status "Done" ที่เปลี่ยนล่าสุด + daily memory notes)
   - Format: bullet list แยกวัน เช่น "เมื่อวาน: ..." / "วันนี้: ..."
   - ถ้าไม่มี task cleared → แสดง "ยังไม่มี task cleared"
2. **📅 ตารางวัน** — Markdown table (เวลา | กิจกรรม | สถานที่)
   - ไม่ต้องแสดง Sleep
3. **⏰ ช่วงเวลาว่าง** — Markdown table (ช่วง | ระยะเวลา) พร้อม 🟢
4. **📋 Todo List** — Markdown table (# | Task | Status | Deadline)
   - แยก In Progress (🔄) กับ Next Up (📌)
5. **🎯 คำแนะนำจาก Prem:**
   - ถ้ามี deadline เร่งด่วน → จัดการ deadline ก่อน + แนะนำช่วงเวลาที่เหมาะ
   - ถ้าเวลาว่างไม่มี deadline → เสนอแผน Agoda เป็นหลัก:
     - ≥ 2 ชม. → HackerRank Practice
     - 30 นาที - 1 ชม. → English Listening
     - ≥ 1 ชม. → Interview Practice
   - จับคู่ช่วงเวลาว่างกับ task/แผน Agoda ที่เหมาะสม
   - ใช้ blockquote (>) และ tone ให้กำลังใจ

---

## Cron Jobs Active

| Job | เวลา (ไทย) | ทำอะไร |
|-----|------------|--------|
| Morning Briefing | 07:00 | Calendar + Notion Todo → Discord (tag Oscar) |
| Webhook Processor | 20:00 | Process pending webhooks (silent) |
| Transaction Summary | 21:00 | สรุป + ถาม category → Discord (tag Oscar) |
| Tech News Digest | 13:00 | Browser+Blogwatcher→สรุปข่าว tech → Discord (tag Oscar) |
| Email Digest | 09:00 | Gmail inbox → filter spam → สรุป actionable emails → Discord (tag Oscar) |

### Discord Tag Rule
- ทุก cron ที่ส่งข้อความรายวัน (Morning Briefing, Transaction Summary) → ต้อง tag `<@713320178615844954>` เสมอ เพื่อแจ้งเตือน Oscar

### Spending Pattern Learning:
- เก็บพฤติกรรมใน `memory/spending-patterns.md`
- ดู เวลา + จำนวนเงิน + วัน เพื่อเดา category
- เช่น: 50฿ ตอน 18:00-21:00 → น่าจะเป็นค่าข้าวเย็น
- ทุกครั้งที่ Oscar ตอบ → บันทึกลง Response History
- ยิ่งมีข้อมูลมาก ยิ่งเดาแม่นขึ้น

### 8PM Workflow:
1. ดึง pending webhooks
2. Parse K+ SMS → เวลา, จำนวน, ประเภท
3. เดา category จาก spending-patterns.md (เวลา + จำนวน + พฤติกรรม)
4. แสดงให้ Oscar ดูพร้อมคำเดา เช่น "50฿ ตอน 22:26 → น่าจะค่าข้าวเย็น 🍽️"
5. Oscar ตอบ approve/แก้ไข → สร้าง transaction + mark PROCESSED
6. บันทึกคำตอบ Oscar ลง spending-patterns.md เพื่อเรียนรู้
