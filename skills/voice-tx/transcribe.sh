#!/bin/bash
# Voice Transaction - Transcribe audio using Groq Whisper API
# Usage: ./transcribe.sh <audio_file> [language]

GROQ_API_KEY="GROQ_API_KEY_REDACTED"
AUDIO_FILE="$1"
LANGUAGE="${2:-th}"

if [ -z "$AUDIO_FILE" ]; then
  echo "Usage: $0 <audio_file> [language]" >&2
  exit 1
fi

if [ ! -f "$AUDIO_FILE" ]; then
  echo "File not found: $AUDIO_FILE" >&2
  exit 1
fi

curl -s "https://api.groq.com/openai/v1/audio/transcriptions" \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F "file=@$AUDIO_FILE" \
  -F "model=whisper-large-v3" \
  -F "language=$LANGUAGE" \
  -F "response_format=json" | jq -r '.text'
