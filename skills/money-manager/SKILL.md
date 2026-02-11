# Money Manager Skill

Parse bank notifications and manage personal finance via webhook/API.

## Quick Reference

| Resource | URL |
|---|---|
| Dashboard | https://76.13.182.44.nip.io/app/ (admin/admin123) |
| Webhook API | https://76.13.182.44.nip.io/api/v1/webhook (no auth) |
| Internal API | http://localhost:8080/api/v1 |
| Project | `/root/webhook-server/` |

## API Endpoints

### Webhooks
```bash
# Pending webhooks
curl -s http://localhost:8080/api/v1/webhooks/pending | jq .

# Mark processed
curl -X PATCH http://localhost:8080/api/v1/webhooks/{id}/status \
  -H "Content-Type: application/json" \
  -d '{"status":"PROCESSED"}'

# Mark failed
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
    "note": "Dinner"
  }'
```

## Account Mapping

| ID | Name | Bank Code | Type |
|---|---|---|---|
| 1 | K+ | KBANK | BANK |
| 2 | SCB Easy | SCB | BANK |
| 3 | Cash | - | CASH |
| 4 | TrueMoney | TMN | EWALLET |

Primary account: KBank suffix 5427 → `account_id=1`

## Category IDs

| ID | Category | Type |
|---|---|---|
| 1 | Food & Dining | EXPENSE |
| 2 | Transport | EXPENSE |
| 3 | Shopping | EXPENSE |
| 4 | Income | INCOME |
| 5 | Bills & Utilities | EXPENSE |
| 6 | Financial | EXPENSE |
| 10 | Transfer | EXPENSE |
| 11 | Ride Hailing | EXPENSE |
| 13 | Food Delivery | EXPENSE |

## K PLUS SMS Format

```text
K PLUS|credit-notice|acct xxx-x-x5427-x amount 50.00 THB date 7 Feb 69 22:27
K PLUS|debit-notice|acct xxx-x-x5427-x amount 50.00 THB date 7 Feb 69 22:26
```

### Parsing Rules
- Bank marker: `K PLUS` → KBANK (`account_id=1`)
- Transaction marker equivalents: credit-like phrase → `INCOME`, debit/transfer-like phrase → `EXPENSE`
- Amount pattern: `amount X.XX THB`
- Date pattern: `date D Mon YY HH:MM`

If payloads are in Thai text, map Thai month abbreviations and convert Buddhist year to Gregorian year explicitly.

## Daily Workflow

### 20:00 — Webhook Processor (silent)
1. `GET /webhooks/pending`
2. Parse message fields
3. Prepare candidates for user confirmation

### 21:00 — Transaction Summary (Discord)
1. Show pending webhooks
2. Ask user for category/note (or skip/delete)
3. Create transaction only after confirmation
4. Mark webhook `PROCESSED`

## Error Handling

If parsing fails:
1. mark webhook as `FAILED`
2. store error details
3. ask user to categorize manually from dashboard
