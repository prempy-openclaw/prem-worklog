---
name: gog
description: Google Workspace helper for Gmail and Calendar via custom Python script with automatic token refresh.
metadata: {}
---

# Gog — Google Workspace Helper (Gmail + Calendar)

Account: `golfpopmei14@gmail.com`

## Calendar Display Policy (Emoji Categorization)

Events are categorized by keywords in the summary:

| Category | Emojis | Keywords |
|---|---|---|
| Sleep | 😴 | sleep, nap |
| Work/Coding | 💻, 🖥️ | work, coding, build, implementation |
| Learning/Education | 📚, 🎓 | learn, study, class, exam, hacker, lng |
| Relax/Personal | 🍔, ☕ | relax, personal, break |
| Meeting/Appointment | 🤝, 📋 | meet, meeting, appointment |
| Sports/Exercise | 🏃, 🏊, 🏋️ | sport, exercise, workout |
| Shopping | 🛒, 🛍️ | shop, shopping, buy |
| Travel/Transport | 🚗, 🚕, ✈️ | travel, commute, ride, go |
| Default | 📌 | no match |

## Setup

Credentials/tokens are configured at:
- Client credentials: `/root/.openclaw/workspace/skills/gog/client_secret.json`
- Helper script: `/root/.openclaw/workspace/skills/gog/gog_helper.py`
- Refresh token: embedded in helper script (file backend)

## Usage

### Gmail

```bash
# List labels
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py gmail-labels

# List unread inbox emails (optional: max, query)
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py gmail-inbox 20 "is:unread"

# Read a specific email
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py gmail-read <message_id>
```

### Calendar (Display)

```bash
# Today's events
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py today

# Specific date (YYYY-MM-DD)
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py date 2026-02-07

# List calendars
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py calendar-list

# Raw events JSON
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py calendar-events
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py calendar-events golfpopmei14@gmail.com 20
```

### Calendar (Management)

```bash
# Create event
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py create "<summary>" "<start_time>" "<end_time>" [location] [description]

# Update event
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py update "<event_id>" [summary] [start] [end] [location] [desc]

# Delete event
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py delete "<event_id>"
```

Time format: ISO 8601 (`YYYY-MM-DDTHH:MM:SS`)

## Token Management

The helper auto-refreshes OAuth tokens:
- cached access token: `/tmp/gog_tokens.json`
- refresh trigger: expiry minus 5-minute buffer
- refresh method: OAuth2 refresh token

## Notes

- Timezone: Asia/Bangkok
- Primary calendar ID: `golfpopmei14@gmail.com`
- Verified: 2026-02-07
