# TOOLS.md - Local Notes

## Voice Transaction (Groq Whisper)

**API:** Groq Whisper large-v3 (ฟรี)
**Script:** `/root/.openclaw/workspace/skills/voice-tx/transcribe.sh`

### Usage
```bash
/root/.openclaw/workspace/skills/voice-tx/transcribe.sh <audio_file> [language]
```

### Workflow
เมื่อ Oscar ส่งเสียง → ถอดเสียง → parse → สร้าง transaction

---

## Claude Code (Coding Assistant)

**Version:** 2.1.34
**API Key:** Configured in `~/.bashrc`
**⚠️ MUST READ:** ก่อนใช้ Claude Code ทุกครั้ง → อ่าน skill `claude-code-mastery` ก่อนเสมอ!
**Skill:** `/root/.openclaw/workspace/skills/claude-code-mastery/SKILL.md`

### Usage
```bash
# Interactive mode
claude

# One-shot command
claude "สร้าง function X ด้วย Go"

# With file context
claude "แก้ bug ใน main.go"
```

### Workflow
เมื่อ Oscar ขอให้เขียน code → ใช้ Claude Code CLI เป็นหลัก → อ่าน claude-code-mastery skill ก่อนทุกครั้ง

---

## Google Workspace (Gog Helper)

**Account:** golfpopmei14@gmail.com

### Display Commands

**Today's events:**
```bash
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py today
```

**Events for specific date (YYYY-MM-DD):**
```bash
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py date 2026-02-07
```

### Management Commands (Create/Update/Delete)

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

**Delete event:**
```bash
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py delete "<event_id>"
```

### Raw JSON Commands

**Gmail Labels:**
```bash
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py gmail-labels
```

**Calendar List:**
```bash
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py calendar-list
```

**Calendar Events:**
```bash
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py calendar-events
# Specific calendar + max results
python3 /root/.openclaw/workspace/skills/gog/gog_helper.py calendar-events golfpopmei14@gmail.com 20
```

### Notes

- User timezone: Asia/Bangkok (Thailand)
- Calendar timezone: Asia/Bangkok
- Token auto-refresh: enabled (refresh token embedded)
- Primary calendar ID: golfpopmei14@gmail.com
