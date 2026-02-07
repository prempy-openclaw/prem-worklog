# Money Manager Skill

Parse bank SMS/notifications and manage personal finance via webhook API.

## Quick Reference

| Resource | URL |
|----------|-----|
| Dashboard | https://76.13.182.44.nip.io/app/ (admin/admin123) |
| Webhook API | https://76.13.182.44.nip.io/api/v1/webhook (no auth) |
| Internal API | http://localhost:8080/api/v1 |
| Project | `/root/webhook-server/` |

## API Endpoints

### Webhooks
```bash
# Get pending webhooks
curl -s http://localhost:8080/api/v1/webhooks/pending | jq .

# Mark as processed
curl -X PATCH http://localhost:8080/api/v1/webhooks/{id}/status \
  -H "Content-Type: application/json" \
  -d '{"status":"PROCESSED"}'

# Mark as failed
curl -X PATCH http://localhost:8080/api/v1/webhooks/{id}/status \
  -H "Content-Type: application/json" \
  -d '{"status":"FAILED"}'
```

### Transactions
```bash
# Create transaction
curl -X POST http://localhost:8080/api/v1/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "raw_webhook_id": "uuid-of-webhook",
    "account_id": 1,
    "amount": "50.00",
    "transaction_type": "EXPENSE",
    "transaction_date": "2026-02-07T22:26:00+07:00",
    "category_id": 1,
    "auto_categorized": false,
    "note": "ข้าวเย็น"
  }'

# Get dashboard summary
curl -s "http://localhost:8080/api/v1/dashboard/summary?month=2026-02" | jq .
```

## Account Mapping

| ID | ชื่อ | Bank Code | ประเภท |
|----|------|-----------|--------|
| 1 | K+ | KBANK | BANK |
| 2 | SCB Easy | SCB | BANK |
| 3 | เงินสด | - | CASH |
| 4 | TrueMoney | TMN | EWALLET |

**Oscar's main account:** KBank suffix 5427 → Account ID 1

## Category IDs

| ID | หมวดหมู่ | ประเภท |
|----|---------|--------|
| 1 | 🍽️ Food & Dining | EXPENSE |
| 2 | 🚗 Transport | EXPENSE |
| 3 | 🛒 Shopping | EXPENSE |
| 4 | 💰 Income | INCOME |
| 5 | 🏠 Bills & Utilities | EXPENSE |
| 6 | 💳 Financial | EXPENSE |
| 10 | 💸 Transfer | EXPENSE |
| 11 | 🚕 Ride Hailing | EXPENSE |
| 13 | 🛵 Food Delivery | EXPENSE |

## K PLUS SMS Format

Oscar ใช้ K PLUS เป็นหลัก format คือ:
```
K PLUS|รายการเงินเข้า|บัญชี xxx-x-x5427-x จำนวนเงิน 50.00 บาท วันที่ 7 ก.พ. 69 22:27 น.
K PLUS|รายการโอน/ถอน|บัญชี xxx-x-x5427-x จำนวนเงิน 50.00 บาท วันที่ 7 ก.พ. 69 22:26 น.
```

### Parsing Rules
| Field | Detection |
|-------|-----------|
| Bank | "K PLUS" → KBANK (account_id: 1) |
| Type | "เงินเข้า" → INCOME, "โอน/ถอน" → EXPENSE |
| Amount | `จำนวนเงิน X.XX บาท` |
| Date | `วันที่ D เดือน YY HH:MM น.` (ก.พ.=Feb, 69=2026) |

### Thai Month Mapping
```
ม.ค.=1, ก.พ.=2, มี.ค.=3, เม.ย.=4, พ.ค.=5, มิ.ย.=6
ก.ค.=7, ส.ค.=8, ก.ย.=9, ต.ค.=10, พ.ย.=11, ธ.ค.=12
```

### Buddhist Year Conversion
ปี 69 = พ.ศ. 2569 = ค.ศ. 2026

## Daily Workflow (Cron Jobs)

### 20:00 - Webhook Processor (Silent)
1. `GET /api/v1/webhooks/pending`
2. Parse K+ text → extract data
3. Save parsed data for 21:00 job

### 21:00 - Transaction Summary (Discord)
1. แสดง pending webhooks ให้ Oscar
2. ถามว่า: "หมวดหมู่อะไร? Note?"
3. Oscar ตอบง่ายๆ เช่น:
   - `1: อาหาร` → category_id: 1
   - `ข้าวเย็น` → note: "ข้าวเย็น", category: Food (auto-detect)
   - `skip` → mark PROCESSED โดยไม่สร้าง transaction
4. Prem สร้าง transaction + mark PROCESSED

### Example Interaction
```
Prem: 💰 มี 1 รายการรอจัดการ:
      1️⃣ K PLUS โอน/ถอน -฿50 (22:26)
      หมวดหมู่อะไร? Note?

Oscar: ข้าวเย็น

Prem: ✅ บันทึกแล้ว! -฿50 ข้าวเย็น (🍽️ Food)
```

## Full Processing Example

```bash
# 1. Get pending webhook
WEBHOOK=$(curl -s http://localhost:8080/api/v1/webhooks/pending | jq -r '.webhooks[0]')
WEBHOOK_ID=$(echo $WEBHOOK | jq -r '.ID')
PAYLOAD=$(echo $WEBHOOK | jq -r '.Payload')

# 2. Parse (example for K PLUS โอน/ถอน 50 บาท)
# Type: EXPENSE (โอน/ถอน)
# Amount: 50.00
# Account: 1 (KBank)
# Date: 2026-02-07T22:26:00+07:00

# 3. Create transaction
curl -X POST http://localhost:8080/api/v1/transactions \
  -H "Content-Type: application/json" \
  -d "{
    \"raw_webhook_id\": \"$WEBHOOK_ID\",
    \"account_id\": 1,
    \"amount\": \"50.00\",
    \"transaction_type\": \"EXPENSE\",
    \"transaction_date\": \"2026-02-07T22:26:00+07:00\",
    \"category_id\": 1,
    \"note\": \"ข้าวเย็น\"
  }"

# 4. Mark processed
curl -X PATCH "http://localhost:8080/api/v1/webhooks/$WEBHOOK_ID/status" \
  -H "Content-Type: application/json" \
  -d '{"status":"PROCESSED"}'
```

## Category Detection Keywords

| Keywords | Category |
|----------|----------|
| 7-eleven, เซเว่น, กาแฟ, coffee, starbucks, อาหาร | 🍽️ Food (1) |
| grab, bolt, bts, mrt, taxi, น้ำมัน | 🚗 Transport (2) |
| lazada, shopee, central, โลตัส | 🛒 Shopping (3) |
| เงินเดือน, salary, โบนัส | 💰 Income (4) |
| ค่าไฟ, ค่าน้ำ, ค่าเน็ต, ค่าโทรศัพท์ | 🏠 Bills (5) |
| โอน, transfer | 💸 Transfer (10) |

## Error Handling

If parsing fails:
1. Mark webhook as `FAILED`
2. Store error in `error_log`
3. Ask Oscar to manually categorize via frontend: `/app/webhooks`
