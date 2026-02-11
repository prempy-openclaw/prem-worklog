# Voice Transaction Skill

## Overview
Convert Oscar's voice notes into finance transactions.

## Transcription
```bash
/root/.openclaw/workspace/skills/voice-tx/transcribe.sh <audio_file> [language]
```
- Default language: `th`
- API: Groq Whisper `large-v3`

## Workflow
1. Oscar sends a voice message (example: "Paid 65 baht for lunch")
2. Transcribe audio to text
3. Parse fields:
   - amount
   - type (`EXPENSE` for paid/transferred, `INCOME` for received)
   - category (keyword + spending patterns)
   - note
4. Confirm with Oscar
5. Create transaction

## Examples
- "Paid 65 baht for lunch" → `EXPENSE`, `65`, `Food & Dining`
- "Grab 45 baht" → `EXPENSE`, `45`, `Ride Hailing`
- "Received transfer 5000" → `INCOME`, `5000` (ask category if needed)
- "Coffee 75 baht" → `EXPENSE`, `75`, `Food & Drinks`
