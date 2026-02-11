#!/usr/bin/env python3
"""
Google API Helper - Handles Gmail and Calendar with automatic token refresh
Supports date filtering and beautiful output with emoji-based categorization
"""
import os
import json
import time
import sys
import datetime
import urllib.request
import urllib.parse
from dateutil import tz

REFRESH_TOKEN = "GOG_REFRESH_TOKEN_REDACTED"
CLIENT_ID = "GOG_CLIENT_ID_REDACTED"
CLIENT_SECRET = "GOG_CLIENT_SECRET_REDACTED"

# Token storage
TOKEN_FILE = "/tmp/gog_tokens.json"
access_token = None
token_expiry = 0

# Calendar color/priority policy (emoji-based)
EVENT_CATEGORIES = {
    # Sleep
    'sleep': ['😴'],
    'ง่อนนอน': ['😴'],
    'sleep': ['😴'],
    
    # Work/Coding
    'work': ['💻', '🖥️'],
    'coding': ['💼'],
    'create': ['💻'],
    'ทำงาน': ['💼'],
    'งาน': ['💼'],
    'จบ': ['💻'],
    'เบ็ต': ['💼'],
    
    # Learning/Education
    'learn': ['📚', '🎓'],
    'learning': ['📚', '🎓'],
    'study': ['📚'],
    'l2': ['📚'],
    'lng': ['📚'],
    'hacker': ['📚', '🔢'],
    'hacker': ['📚'],
    'intregated': ['📚'],
    'รียน': ['📚'],
    
    # Relax/Personal
    'relax': ['🍔', '☕'],
    'personal': ['🍔'],
    'พักผ่อน': ['🍔'],
    'ท่อง': ['🍔'],
    
    # Meetings/Appointments
    'meet': ['🤝', '📋'],
    'meeting': ['🤝', '📋'],
    'appointment': ['🤝', '📋'],
    'ประชุม': ['🤝'],
    
    # Sports/Exercise
    'sport': ['🏃', '🏊', '🏋️'],
    'exercise': ['🏃', '🏊', '🏋️'],
    'ฟิต': ['🏃'],
    
    # Shopping/Errands
    'shop': ['🛒', '🛍️'],
    'shopping': ['🛒', '🛍️'],
    'ซื้อ': ['🛒'],
    
    # Travel/Transport
    'travel': ['🚗', '🚕', '✈️'],
    'go': ['🚗'],
    'ไป': ['🚗'],
}

# Keywords mapping to categories
KEYWORD_TO_CATEGORY = {
    'sleep': 'sleep',
    'ง่อน': 'sleep',
    'นอน': 'sleep',
    
    'work': 'work',
    'งาน': 'work',
    'coding': 'work',
    'เขียนโค้ด': 'work',
    'create': 'work',
    'ทำงาน': 'work',
    'จบ': 'work',
    'เบ็ต': 'work',
    
    'learn': 'learn',
    'study': 'learn',
    'learning': 'learn',
    'รียน': 'learn',
    'l2': 'learn',
    'lng': 'learn',
    'hacker': 'learn',
    'intregated': 'learn',
    
    'relax': 'relax',
    'personal': 'relax',
    'พักผ่อน': 'relax',
    'ท่อง': 'relax',
    
    'meet': 'meet',
    'meeting': 'meet',
    'ประชุม': 'meet',
    
    'sport': 'sport',
    'exercise': 'sport',
    'ฟิต': 'sport',
    
    'shop': 'shop',
    'shopping': 'shop',
    'ซื้อ': 'shop',
    
    'travel': 'travel',
    'go': 'travel',
    'ไป': 'travel',
}

def get_event_emoji(summary):
    """Get emoji for event based on keywords in summary"""
    if not summary:
        return '📌'
    
    summary_lower = summary.lower()
    
    # Check for exact keywords
    for keyword, category in KEYWORD_TO_CATEGORY.items():
        if keyword in summary_lower:
            emojis = EVENT_CATEGORIES.get(category, ['📌'])
            return emojis[0] if emojis else '📌'
    
    # Check partial matches in event categories
    for category, emojis in EVENT_CATEGORIES.items():
        if category in summary_lower:
            return emojis[0] if emojis else '📌'
    
    # Default
    return '📌'

def load_tokens():
    """Load tokens from file"""
    global access_token, token_expiry
    try:
        with open(TOKEN_FILE, 'r') as f:
            data = json.load(f)
            access_token = data.get('access_token')
            token_expiry = data.get('expiry', 0)
    except:
        pass

def save_tokens(at, expires_in):
    """Save tokens to file"""
    data = {
        'access_token': at,
        'expiry': int(time.time()) + expires_in
    }
    with open(TOKEN_FILE, 'w') as f:
        json.dump(data, f)

def get_access_token():
    """Get valid access token, refresh if needed"""
    global access_token, token_expiry

    if not access_token:
        load_tokens()

    if access_token and token_expiry > int(time.time()) + 300:
        return access_token

    data = urllib.parse.urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': REFRESH_TOKEN,
        'grant_type': 'refresh_token'
    }).encode()

    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=data,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            access_token = result['access_token']
            expires_in = result.get('expires_in', 3600)
            save_tokens(access_token, expires_in)
            return access_token
    except Exception as e:
        print(f"Error refreshing token: {e}", file=sys.stderr)
        sys.exit(1)

def gmail_labels():
    """List Gmail labels"""
    token = get_access_token()
    req = urllib.request.Request(
        "https://www.googleapis.com/gmail/v1/users/me/labels",
        headers={'Authorization': f'Bearer {token}'}
    )

    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print(json.dumps(result, indent=2))

def gmail_inbox(max_results=10, query="is:unread"):
    """List Gmail messages from inbox"""
    token = get_access_token()
    encoded_query = urllib.parse.quote(query)
    req = urllib.request.Request(
        f"https://www.googleapis.com/gmail/v1/users/me/messages?maxResults={max_results}&q={encoded_query}",
        headers={'Authorization': f'Bearer {token}'}
    )

    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())

    messages = result.get('messages', [])
    if not messages:
        print("📭 ไม่มีอีเมลใหม่")
        return

    print(f"📬 อีเมลที่ยังไม่อ่าน ({len(messages)} รายการ):\n")
    for msg in messages:
        msg_req = urllib.request.Request(
            f"https://www.googleapis.com/gmail/v1/users/me/messages/{msg['id']}?format=metadata&metadataHeaders=From&metadataHeaders=Subject&metadataHeaders=Date",
            headers={'Authorization': f'Bearer {token}'}
        )
        with urllib.request.urlopen(msg_req) as msg_resp:
            msg_data = json.loads(msg_resp.read().decode())

        headers = {h['name']: h['value'] for h in msg_data.get('payload', {}).get('headers', [])}
        subject = headers.get('Subject', '(no subject)')
        sender = headers.get('From', 'unknown')
        date = headers.get('Date', '')
        snippet = msg_data.get('snippet', '')
        labels = msg_data.get('labelIds', [])

        # Detect spam/promo
        category = ''
        if 'CATEGORY_PROMOTIONS' in labels:
            category = '📢 Promo'
        elif 'CATEGORY_SOCIAL' in labels:
            category = '👥 Social'
        elif 'CATEGORY_UPDATES' in labels:
            category = '🔔 Update'
        elif 'CATEGORY_FORUMS' in labels:
            category = '💬 Forum'
        elif 'SPAM' in labels:
            category = '🚫 Spam'
        else:
            category = '📧 Primary'

        print(f"  {category} | {subject}")
        print(f"    From: {sender}")
        print(f"    Date: {date}")
        print(f"    Preview: {snippet[:120]}...")
        print(f"    ID: {msg['id']}")
        print()

def gmail_read(msg_id):
    """Read a specific Gmail message"""
    token = get_access_token()
    req = urllib.request.Request(
        f"https://www.googleapis.com/gmail/v1/users/me/messages/{msg_id}?format=full",
        headers={'Authorization': f'Bearer {token}'}
    )

    with urllib.request.urlopen(req) as response:
        msg_data = json.loads(response.read().decode())

    headers = {h['name']: h['value'] for h in msg_data.get('payload', {}).get('headers', [])}
    subject = headers.get('Subject', '(no subject)')
    sender = headers.get('From', 'unknown')
    date = headers.get('Date', '')

    # Extract body
    import base64
    body = ''
    payload = msg_data.get('payload', {})
    if 'body' in payload and payload['body'].get('data'):
        body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='replace')
    elif 'parts' in payload:
        for part in payload['parts']:
            if part.get('mimeType') == 'text/plain' and part.get('body', {}).get('data'):
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='replace')
                break
        if not body:
            for part in payload['parts']:
                if part.get('mimeType') == 'text/html' and part.get('body', {}).get('data'):
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='replace')
                    break

    print(f"📧 {subject}")
    print(f"From: {sender}")
    print(f"Date: {date}")
    print(f"\n{body[:3000]}")

def calendar_list():
    """List calendars"""
    token = get_access_token()
    req = urllib.request.Request(
        "https://www.googleapis.com/calendar/v3/users/me/calendarList",
        headers={'Authorization': f'Bearer {token}'}
    )

    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print(json.dumps(result, indent=2))

def calendar_events(calendar_id='primary', max_results=10, date_filter=None):
    """List calendar events with optional date filtering"""
    token = get_access_token()

    params = {
        'maxResults': max_results,
        'orderBy': 'startTime',
        'singleEvents': 'true'
    }

    # Add date filter if provided
    if date_filter:
        try:
            # Parse date as YYYY-MM-DD
            dt = datetime.datetime.strptime(date_filter, '%Y-%m-%d').date()
            tzinfo = tz.gettz('Asia/Bangkok')
            dt_start = datetime.datetime.combine(dt, datetime.time.min).replace(tzinfo=tzinfo)
            dt_end = dt_start + datetime.timedelta(days=1)

            params['timeMin'] = dt_start.strftime('%Y-%m-%dT%H:%M:%S%z')
            params['timeMax'] = dt_end.strftime('%Y-%m-%dT%H:%M:%S%z')
            params['timeZone'] = 'Asia/Bangkok'
        except ValueError:
            print(f"Invalid date format: {date_filter}. Use YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)

    url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(
        url,
        headers={'Authorization': f'Bearer {token}'}
    )

    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print(json.dumps(result, indent=2))

def calendar_events_display(calendar_id='primary', max_results=10, date_filter=None):
    """Display calendar events in a beautiful format with emoji categorization"""
    token = get_access_token()

    params = {
        'maxResults': max_results,
        'orderBy': 'startTime',
        'singleEvents': 'true'
    }

    date_obj = None

    if date_filter:
        try:
            date_obj = datetime.datetime.strptime(date_filter, '%Y-%m-%d').date()
            tzinfo = tz.gettz('Asia/Bangkok')
            dt_start = datetime.datetime.combine(date_obj, datetime.time.min).replace(tzinfo=tzinfo)
            dt_end = dt_start + datetime.timedelta(days=1)

            params['timeMin'] = dt_start.strftime('%Y-%m-%dT%H:%M:%S%z')
            params['timeMax'] = dt_end.strftime('%Y-%m-%dT%H:%M:%S%z')
            params['timeZone'] = 'Asia/Bangkok'
        except ValueError:
            print(f"❌ Invalid date format: {date_filter}. Use YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)

    url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(
        url,
        headers={'Authorization': f'Bearer {token}'}
    )

    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        items = data.get('items', [])

        # Build date string
        if date_filter:
            dt = date_obj
            days_th = ['จันทร์', 'อังคาร', 'พุธ', 'พฤหัสบดี', 'ศุกร์', 'เสาร์', 'อาทิตย์']
            months_th = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
                        'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม']
            date_str = f'{dt.day} {months_th[dt.month-1]} {dt.year+543} (วัน{days_th[dt.weekday()]})'
            print(f'\n📅 ตารางวันที่ {date_str}\n')
        else:
            now = datetime.datetime.now(tz.gettz('Asia/Bangkok'))
            print(f'\n📅 Upcoming Events (ล่าสุด):\n')

        if not items:
            print('  🎉 ไม่มีนัด!\n')
            return

        # Sort by start time
        items.sort(key=lambda x: x.get('start', {}).get('dateTime') or x.get('start', {}).get('date'))

        # Display events in table format
        if not items:
            print('🎉 ไม่มีนัดหมายวันนี้!\n')
            return

        # Print table header
        print('┌────────────┬────────────┬────────────────────────────┬─────────────┬──────────────┬─────────────┐')
        print('│ เวลา     │ กิจกรรม   │ รายละเอียด             │ สถานที่   │ รายละเอียด  │')
        print('├────────────┼────────────┼────────────────────────────┼─────────────┼──────────────┼─────────────┤')

        # Display each event
        for e in items:
            start = e.get('start', {})
            end = e.get('end', {})
            summary = e.get('summary', 'ไม่มีชื่อ')
            location = e.get('location', '')
            description = e.get('description', '')

            # Get emoji based on summary
            emoji = get_event_emoji(summary)

            # Parse time
            if 'dateTime' in start:
                dt_start = datetime.datetime.fromisoformat(start['dateTime'].replace('Z', '+00:00'))
                dt_end = datetime.datetime.fromisoformat(end['dateTime'].replace('Z', '+00:00'))
                dt_start = dt_start.astimezone(tz.gettz('Asia/Bangkok'))
                dt_end = dt_end.astimezone(tz.gettz('Asia/Bangkok'))

                time_range = f'{dt_start.strftime("%H:%M")} - {dt_end.strftime("%H:%M")}'
            elif 'date' in start:
                time_range = 'ทั้งวัน'
            else:
                time_range = ''

            # Truncate for table display
            summary_short = summary[:20] if len(summary) > 20 else summary
            location_short = location[:12] if len(location) > 12 else location
            desc_short = description[:20] if description and len(description) > 20 else (description or '')

            # Print row
            print(f'│ {time_range:10} │ {emoji:10} │ {summary_short:20} │ {location_short:11} │ {desc_short:12} │')

        # Print table footer
        print('└────────────┴────────────┴────────────────────────────┴─────────────┴──────────────┴─────────────┘')
        print()

        # Calculate and display free time slots
        # Working hours: 09:00-18:00 and 20:00-23:00 only
        bkk = tz.gettz('Asia/Bangkok')
        busy_slots = []
        for e in items:
            start = e.get('start', {})
            end = e.get('end', {})
            if 'dateTime' in start:
                dt_s = datetime.datetime.fromisoformat(start['dateTime'].replace('Z', '+00:00')).astimezone(bkk)
                dt_e = datetime.datetime.fromisoformat(end['dateTime'].replace('Z', '+00:00')).astimezone(bkk)
                busy_slots.append((dt_s, dt_e))

        if date_filter:
            date_obj = datetime.datetime.strptime(date_filter, '%Y-%m-%d').replace(tzinfo=bkk)

            # Define working windows
            work_windows = [
                (date_obj.replace(hour=9, minute=0), date_obj.replace(hour=18, minute=0)),
                (date_obj.replace(hour=20, minute=0), date_obj.replace(hour=23, minute=0)),
            ]

            busy_slots.sort(key=lambda x: x[0])
            free_slots = []

            for win_start, win_end in work_windows:
                current = win_start
                for bs, be in busy_slots:
                    # Skip busy slots outside this window
                    if be <= win_start or bs >= win_end:
                        continue
                    # Clamp to window
                    bs_clamped = max(bs, win_start)
                    be_clamped = min(be, win_end)
                    if bs_clamped > current:
                        duration = (bs_clamped - current).total_seconds() / 60
                        if duration >= 30:
                            free_slots.append((current, bs_clamped, int(duration)))
                    current = max(current, be_clamped)
                # Remaining time in window
                if current < win_end:
                    duration = (win_end - current).total_seconds() / 60
                    if duration >= 30:
                        free_slots.append((current, win_end, int(duration)))

            if free_slots:
                print('⏰ ช่วงเวลาว่าง:')
                for fs, fe, dur in free_slots:
                    hours = dur // 60
                    mins = dur % 60
                    dur_str = f'{hours}ชม.' if mins == 0 else (f'{hours}ชม.{mins}นาที' if hours > 0 else f'{mins}นาที')
                    print(f'  🟢 {fs.strftime("%H:%M")} - {fe.strftime("%H:%M")} ({dur_str})')
                print()
            else:
                print('⏰ ไม่มีช่วงเวลาว่างวันนี้\n')

def calendar_create(calendar_id='primary', summary='', start_time='', end_time='', location='', description=''):
    """Create a calendar event"""
    token = get_access_token()

    if not summary:
        print("❌ Error: Summary is required", file=sys.stderr)
        sys.exit(1)

    if not start_time:
        print("❌ Error: Start time is required (format: YYYY-MM-DDTHH:MM:SS)", file=sys.stderr)
        sys.exit(1)

    if not end_time:
        print("❌ Error: End time is required (format: YYYY-MM-DDTHH:MM:SS)", file=sys.stderr)
        sys.exit(1)

    # Build event object
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Asia/Bangkok'
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Asia/Bangkok'
        }
    }

    if location:
        event['location'] = location

    if description:
        event['description'] = description

    req = urllib.request.Request(
        f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events",
        data=json.dumps(event).encode(),
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        },
        method='POST'
    )

    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print(f"✅ Event created successfully!")
        print(f"   Title: {summary}")
        print(f"   Time: {start_time} - {end_time}")
        if location:
            print(f"   Location: {location}")
        print(f"   Event ID: {result.get('id')}")
        print(f"   HTML Link: {result.get('htmlLink')}")

def calendar_update(calendar_id='primary', event_id='', summary=None, start_time=None, end_time=None, location=None, description=None):
    """Update a calendar event"""
    token = get_access_token()

    if not event_id:
        print("❌ Error: Event ID is required", file=sys.stderr)
        sys.exit(1)

    # Get existing event
    req = urllib.request.Request(
        f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events/{event_id}",
        headers={'Authorization': f'Bearer {token}'}
    )

    with urllib.request.urlopen(req) as response:
        event = json.loads(response.read().decode())

    # Update fields
    if summary:
        event['summary'] = summary
    if start_time:
        event['start']['dateTime'] = start_time
    if end_time:
        event['end']['dateTime'] = end_time
    if location is not None:
        event['location'] = location
    if description is not None:
        event['description'] = description

    # Send update
    req = urllib.request.Request(
        f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events/{event_id}",
        data=json.dumps(event).encode(),
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        },
        method='PATCH'
    )

    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print(f"✅ Event updated successfully!")
        print(f"   Event ID: {event_id}")
        print(f"   HTML Link: {result.get('htmlLink')}")

def calendar_delete(calendar_id='primary', event_id=''):
    """Delete a calendar event"""
    token = get_access_token()

    if not event_id:
        print("❌ Error: Event ID is required", file=sys.stderr)
        sys.exit(1)

    req = urllib.request.Request(
        f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events/{event_id}",
        headers={'Authorization': f'Bearer {token}'},
        method='DELETE'
    )

    with urllib.request.urlopen(req) as response:
        if response.status == 204:
            print(f"✅ Event {event_id} deleted successfully!")
        else:
            print(f"❌ Failed to delete event. Status: {response.status}", file=sys.stderr)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: gog_helper.py <command>")
        print("\nDisplay Commands:")
        print("  today [cal_id]                   Display today's events")
        print("  date <YYYY-MM-DD> [cal_id]       Display events for specific date")
        print("\nManagement Commands:")
        print("  create <summary> <start> <end> [location] [description]  Create event")
        print("  update <event_id> [summary] [start] [end] [location] [desc]  Update event")
        print("  delete <event_id>                                                 Delete event")
        print("\nGmail Commands:")
        print("  gmail-inbox [max] [query]         List unread emails (default: 10, is:unread)")
        print("  gmail-read <msg_id>               Read specific email")
        print("  gmail-labels                      List Gmail labels")
        print("\nRaw Commands (JSON output):")
        print("  calendar-list                    List calendars")
        print("  calendar-events [cal_id] [max]    List events (JSON)")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'gmail-inbox':
        max_r = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        query = sys.argv[3] if len(sys.argv) > 3 else 'is:unread'
        gmail_inbox(max_r, query)
    elif command == 'gmail-read':
        if len(sys.argv) < 3:
            print("Usage: gmail-read <msg_id>", file=sys.stderr)
            sys.exit(1)
        gmail_read(sys.argv[2])
    elif command == 'gmail-labels':
        gmail_labels()
    elif command == 'calendar-list':
        calendar_list()
    elif command == 'calendar-events':
        cal_id = sys.argv[2] if len(sys.argv) > 2 else 'primary'
        max_results = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        calendar_events(cal_id, max_results)
    elif command == 'today':
        cal_id = sys.argv[2] if len(sys.argv) > 2 else 'primary'
        calendar_events_display(cal_id, 100, datetime.datetime.now(tz.gettz('Asia/Bangkok')).strftime('%Y-%m-%d'))
    elif command == 'date':
        if len(sys.argv) < 3:
            print("Error: date required. Usage: date <YYYY-MM-DD> [cal_id]", file=sys.stderr)
            sys.exit(1)
        date_filter = sys.argv[2]
        cal_id = sys.argv[3] if len(sys.argv) > 3 else 'primary'
        calendar_events_display(cal_id, 100, date_filter)
    elif command == 'create':
        if len(sys.argv) < 5:
            print("Usage: create <summary> <start> <end> [location] [description]", file=sys.stderr)
            print("  Example: create 'Meeting' '2026-02-07T10:00:00' '2026-02-07T11:00:00' 'Room A' 'Discuss project'", file=sys.stderr)
            sys.exit(1)
        summary = sys.argv[2]
        start_time = sys.argv[3]
        end_time = sys.argv[4]
        location = sys.argv[5] if len(sys.argv) > 5 else ''
        description = sys.argv[6] if len(sys.argv) > 6 else ''
        calendar_create('primary', summary, start_time, end_time, location, description)
    elif command == 'update':
        if len(sys.argv) < 3:
            print("Usage: update <event_id> [summary] [start] [end] [location] [desc]", file=sys.stderr)
            print("  Example: update 'abc123' 'New Title' '2026-02-07T10:00:00' '2026-02-07T11:00:00'", file=sys.stderr)
            sys.exit(1)
        event_id = sys.argv[2]
        summary = sys.argv[3] if len(sys.argv) > 3 else None
        start_time = sys.argv[4] if len(sys.argv) > 4 else None
        end_time = sys.argv[5] if len(sys.argv) > 5 else None
        location = sys.argv[6] if len(sys.argv) > 6 else None
        description = sys.argv[7] if len(sys.argv) > 7 else None
        calendar_update('primary', event_id, summary, start_time, end_time, location, description)
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Usage: delete <event_id>", file=sys.stderr)
            sys.exit(1)
        event_id = sys.argv[2]
        calendar_delete('primary', event_id)
    else:
        print(f"❌ Unknown command: {command}", file=sys.stderr)
        sys.exit(1)
