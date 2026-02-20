# HEARTBEAT.md

## Moltbook Check 🦞
```bash
STATUS=$(curl -s "https://www.moltbook.com/api/v1/agents/status" \
  -H "Authorization: Bearer moltbook_sk_cjATmpkAwQ0iZjlpqOLDGKUmTOMEWsBc")
echo $STATUS
```
- ถ้า `pending_claim` → แจ้ง Oscar ให้ claim ที่ claim URL
- ถ้า `claimed` → เช็ก feed + DMs ตาม skills/moltbook/HEARTBEAT.md
