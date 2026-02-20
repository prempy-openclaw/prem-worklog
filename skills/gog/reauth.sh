#!/bin/bash
# Google OAuth Re-Auth Script
# ใช้เมื่อ refresh token หมดอายุหรือถูก revoke
# ต้องมี CLIENT_ID และ CLIENT_SECRET จาก Google Cloud Console

set -e

echo "=== Google OAuth Re-Auth ==="
echo ""

# รับค่าจาก user หรือ env
CLIENT_ID="${GOG_CLIENT_ID:-}"
CLIENT_SECRET="${GOG_CLIENT_SECRET:-}"

if [ -z "$CLIENT_ID" ]; then
  read -p "Enter CLIENT_ID (from Google Cloud Console): " CLIENT_ID
fi
if [ -z "$CLIENT_SECRET" ]; then
  read -p "Enter CLIENT_SECRET: " CLIENT_SECRET
fi

SCOPE="https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/calendar"
REDIRECT_URI="urn:ietf:wg:oauth:2.0:oob"

# สร้าง auth URL
AUTH_URL="https://accounts.google.com/o/oauth2/auth?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${SCOPE}'))")&response_type=code&access_type=offline&prompt=consent"

echo "เปิดลิงก์นี้ใน browser:"
echo ""
echo "$AUTH_URL"
echo ""
read -p "วาง Authorization Code ที่ได้มา: " AUTH_CODE

# Exchange code for tokens
RESPONSE=$(curl -s -X POST "https://oauth2.googleapis.com/token" \
  -d "code=${AUTH_CODE}" \
  -d "client_id=${CLIENT_ID}" \
  -d "client_secret=${CLIENT_SECRET}" \
  -d "redirect_uri=${REDIRECT_URI}" \
  -d "grant_type=authorization_code")

REFRESH_TOKEN=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('refresh_token','ERROR'))")

if [ "$REFRESH_TOKEN" = "ERROR" ]; then
  echo "❌ Error:"
  echo "$RESPONSE"
  exit 1
fi

echo ""
echo "✅ ได้ Refresh Token แล้ว!"
echo ""
echo "เพิ่มลงใน /root/.env:"
echo ""
echo "GOG_CLIENT_ID=${CLIENT_ID}"
echo "GOG_CLIENT_SECRET=${CLIENT_SECRET}"
echo "GOG_REFRESH_TOKEN=${REFRESH_TOKEN}"

# เพิ่มลง /root/.env อัตโนมัติ
if [ -f /root/.env ]; then
  # ลบบรรทัดเก่าถ้ามี
  sed -i '/^GOG_CLIENT_ID=/d; /^GOG_CLIENT_SECRET=/d; /^GOG_REFRESH_TOKEN=/d' /root/.env
  echo "" >> /root/.env
  echo "# Google OAuth (re-authed $(date -u +%Y-%m-%d))" >> /root/.env
  echo "GOG_CLIENT_ID=${CLIENT_ID}" >> /root/.env
  echo "GOG_CLIENT_SECRET=${CLIENT_SECRET}" >> /root/.env
  echo "GOG_REFRESH_TOKEN=${REFRESH_TOKEN}" >> /root/.env
  echo ""
  echo "✅ บันทึกลง /root/.env แล้วครับ"
fi

# Update client_secret.json
cat > /root/.openclaw/workspace/skills/gog/client_secret.json << EOF
{"installed":{"client_id":"${CLIENT_ID}","client_secret":"${CLIENT_SECRET}","redirect_uris":["urn:ietf:wg:oauth:2.0:oob"],"auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token"}}
EOF

echo "✅ client_secret.json updated"
echo ""
echo "ทดสอบ: GOG_REFRESH_TOKEN=${REFRESH_TOKEN} GOG_CLIENT_ID=${CLIENT_ID} GOG_CLIENT_SECRET=${CLIENT_SECRET} python3 /root/.openclaw/workspace/skills/gog/gog_helper.py today"
