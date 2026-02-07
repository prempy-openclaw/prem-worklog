---
name: gog
description: Google Workspace helper for Gmail and Calendar via custom Python script with automatic token refresh.
metadata: {}
---

# Gog - Google Workspace Helper (Gmail + Calendar)

Account: `golfpopmei14@gmail.com`

## Calendar Display Policy (Emoji-Based Categorization)

Events are categorized using emojis based on keywords in the summary:

| Category | Emojis | Keywords |
|-----------|---------|-----------|
| Sleep | 😴 | sleep, นอน, ง่อน |
| Work/Coding | 💻, 🖥️ | work, งาน, coding, create, ทำงาน, จบ, เบ็ต |
| Learning/Education | 📚, 🎓 | learn, study, learning, รียน, l2, lng, hacker, intregated |
| Relax/Personal | 🍔, ☕ | relax, personal, พักผ่อน, ท่อง |
| Meeting/Appointment | 🤝, 📋 | meet, meeting, appointment, ประชุม |
| Sports/Exercise | 🏃, 🏊, 🏋️ | sport, exercise, ฟิต |
| Shopping | 🛒, 🛍️ | shop, shopping, ซื้อ |
| Travel/Transport | 🚗, 🚕, ✈️ | travel, go, ไป |
| Default | 📌 | No matching keywords |

## Setup

Credentials and tokens are configured at:
- Client credentials: `/root/.openclaw/workspace/skills/gog/client_secret.json`
- Helper script: `/root/.openclaw/workspace/skills/gog/gog_helper.py`
- Refresh token: Embedded in helper script (file backend)

## Usage

### Gmail

**List labels:**
```bash
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py gmail-labels
```

### Calendar - Display

**Today's events:**
```bash
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py today
```

**Events for specific date (YYYY-MM-DD):**
```bash
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py date 2026-02-07
```

**List calendars:**
```bash
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py calendar-list
```

**Raw JSON output (default 10 events):**
```bash
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py calendar-events
```

**Raw JSON output (specific calendar, max results):**
```bash
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py calendar-events golfpopmei14@gmail.com 20
```

### Calendar - Management (Create/Update/Delete)

**Create event:**
```bash
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py create "<summary>" "<start_time>" "<end_time>" [location] [description]
```
Example:
```bash
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py create "Meeting" "2026-02-07T10:00:00" "2026-02-07T11:00:00" "Room A" "Discuss project"
```

**Update event:**
```bash
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py update "<event_id>" [summary] [start] [end] [location] [desc]
```
Example:
```bash
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py update "abc123" "New Title" "2026-02-07T10:00:00" "2026-02-07T11:00:00" "Room B"
```

**Delete event:**
```bash
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py delete "<event_id>"
```

Note: Time format should be ISO 8601: `YYYY-MM-DDTHH:MM:SS`

## Token Management

The helper script handles automatic token refresh:
- Stores cached access token in `/tmp/gog_tokens.json`
- Refreshes token when expired (1 hour lifetime + 5 min buffer)
- Uses OAuth2 refresh token for seamless operation

## Notes

- Timezone: Asia/Bangkok (from calendar settings)
- Primary calendar ID: `golfpopmei14@gmail.com`
- Account verified: 2026-02-07
