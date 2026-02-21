#!/usr/bin/env python3
"""
Notion API Helper - Connect to Notion and query databases with beautiful display
Requires NOTION_API_KEY environment variable
"""
import json
import os
import sys
import urllib.request
import urllib.parse
import datetime
from dateutil import tz

NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "")

def get_page(page_id):
    """Get a Notion page"""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    req = urllib.request.Request(
        url,
        headers={
            'Authorization': f'Bearer {NOTION_API_KEY}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json'
        }
    )

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def get_database(database_id):
    """Get database schema"""
    url = f"https://api.notion.com/v1/databases/{database_id}"
    req = urllib.request.Request(
        url,
        headers={
            'Authorization': f'Bearer {NOTION_API_KEY}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json'
        }
    )

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def query_database(database_id, filter_json=None):
    """Query a database"""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"

    payload = {}
    
    if filter_json:
        try:
            payload['filter'] = json.loads(filter_json)
        except json.JSONDecodeError:
            print(f"Invalid filter JSON: {filter_json}", file=sys.stderr)
            sys.exit(1)

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            'Authorization': f'Bearer {NOTION_API_KEY}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json'
        },
        method='POST'
    )

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def search_todo_lists():
    """Search for Todo databases"""
    url = "https://api.notion.com/v1/search"

    payload = {
        "filter": {
            "property": "object",
            "value": "database"
        },
        "query": "todo"
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            'Authorization': f'Bearer {NOTION_API_KEY}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json'
        },
        method='POST'
    )

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def display_todo_list(database_id, status_filter=None, limit=None):
    """Display todo list in beautiful format"""
    result = query_database(database_id)
    results = result.get('results', [])
    
    # Apply filters locally (after fetching all)
    if status_filter:
        results = [r for r in results if r.get('properties', {}).get('Status', {}).get('select', {}).get('name', '').lower() == status_filter.lower()]
    
    if limit:
        results = results[:limit]
    
    print(f'📋 Todo List ({len(results)} items):\n')
    
    if not results:
        print('  🎉 ไม่มี tasks!\n')
        return
    
    # Display tasks
    for i, item in enumerate(results, 1):
        props = item.get('properties', {})
        
        # Get name (title)
        name_prop = props.get('Name', {})
        if 'title' in name_prop and name_prop['title']:
            name_text = name_prop['title'][0]['text']['content'] if name_prop['title'][0].get('text') else 'No name'
        else:
            name_text = 'No name'
        
        # Get status
        status_prop = props.get('Status', {})
        status = status_prop['select']['name'] if 'select' in status_prop and status_prop['select'] else 'No status'
        
        # Get priority
        priority_prop = props.get('Priority', {})
        priority = priority_prop['select']['name'] if 'select' in priority_prop and priority_prop['select'] else ''
        
        # Get due date
        due_prop = props.get('Due Date', {})
        if 'date' in due_prop and due_prop['date']:
            due_str = due_prop['date'].get('start', 'No due date')
            # Format date
            try:
                if 'T' in due_str:
                    dt = datetime.datetime.fromisoformat(due_str.replace('Z', '+00:00'))
                    dt = dt.astimezone(tz.gettz('Asia/Bangkok'))
                    due_str = dt.strftime('%d %b %Y')
            except:
                pass
        else:
            due_str = ''
        
        # Status emoji
        status_emoji = ''
        if status == 'Completed':
            status_emoji = '✅'
        elif status == 'In Progress':
            status_emoji = '🔄'
        elif status == 'Next Up':
            status_emoji = '🔜'
        elif status == 'End':
            status_emoji = '❌'
        
        # Priority emoji
        priority_emoji = ''
        if 'High' in priority:
            priority_emoji = '🔥'
        elif 'Medium' in priority:
            priority_emoji = '⚠️'
        elif 'Low' in priority:
            priority_emoji = '📉'
        
        # Display
        print(f'{i}. {status_emoji} {name_text}')
        
        if priority_emoji:
            print(f'   {priority_emoji} Priority: {priority}')
        
        if due_str:
            print(f'   📅 Due: {due_str}')
        
        print()

def display_todo_simple(database_id, max_items=10):
    """Display todo list in simple format - only Next Up and In Progress"""
    # Use Notion API filter directly for better performance
    filter_json = json.dumps({
        "or": [
            {"property": "Status", "select": {"equals": "Next Up"}},
            {"property": "Status", "select": {"equals": "In Progress"}}
        ]
    })
    result = query_database(database_id, filter_json)
    results = result.get('results', [])
    
    def get_status_name(item):
        status = item.get('properties', {}).get('Status', {})
        if status and status.get('select'):
            return status.get('select', {}).get('name', '')
        return ''
    
    def get_priority_name(item):
        priority = item.get('properties', {}).get('Priority', {})
        if priority and priority.get('select'):
            return priority.get('select', {}).get('name', '')
        return ''
    
    def get_due_date(item):
        due_prop = item.get('properties', {}).get('Due Date', {})
        if due_prop and due_prop.get('date'):
            return due_prop['date'].get('start', '')
        return ''
    
    # Sort by priority and status
    priority_order = {'High 🔥': 0, 'High ??': 1, 'Medium': 2, 'Low': 3, '': 4}
    status_order = {'In Progress': 0, 'Next Up': 1}
    
    results.sort(key=lambda x: (
        status_order.get(get_status_name(x), 99),
        priority_order.get(get_priority_name(x), 99)
    ))
    
    # Limit items
    results = results[:max_items]
    
    # Count by status
    in_progress = len([r for r in results if get_status_name(r) == 'In Progress'])
    next_up = len([r for r in results if get_status_name(r) == 'Next Up'])
    
    print(f'📋 Todo List ({in_progress} In Progress, {next_up} Next Up):\n')
    
    if not results:
        print('  🎉 ไม่มี active tasks!\n')
        return
    
    # Display tasks
    for i, item in enumerate(results, 1):
        props = item.get('properties', {})
        
        # Get name (title)
        name_prop = props.get('Name', {})
        if 'title' in name_prop and name_prop['title']:
            name_text = name_prop['title'][0]['text']['content'] if name_prop['title'][0].get('text') else 'No name'
        else:
            name_text = 'No name'
        
        # Get status
        status = get_status_name(item)
        status_emoji = '🔄' if status == 'In Progress' else '📌'
        
        # Get priority
        priority = get_priority_name(item)
        priority_emoji = ''
        if 'High' in priority:
            priority_emoji = '🔥'
        elif priority == 'Medium':
            priority_emoji = '⚠️'
        elif priority == 'Low':
            priority_emoji = '🟢'
        
        # Get due date
        due_str = get_due_date(item)
        due_display = ''
        if due_str:
            try:
                due_date = datetime.datetime.fromisoformat(due_str.replace('Z', '+00:00'))
                today = datetime.datetime.now(tz.gettz('Asia/Bangkok')).replace(hour=0, minute=0, second=0, microsecond=0)
                due_local = due_date.astimezone(tz.gettz('Asia/Bangkok')).replace(hour=0, minute=0, second=0, microsecond=0)
                
                diff = (due_local - today).days
                if diff < 0:
                    due_display = f' ⚠️ เลย {abs(diff)} วัน!'
                elif diff == 0:
                    due_display = ' 📅 วันนี้!'
                elif diff == 1:
                    due_display = ' 📅 พรุ่งนี้'
                elif diff <= 7:
                    due_display = f' 📅 อีก {diff} วัน'
                else:
                    due_display = f' 📅 {due_str}'
            except:
                due_display = f' 📅 {due_str}'
        
        # Print task
        print(f'{i}. {status_emoji} {name_text}')
        if priority_emoji:
            print(f'   {priority_emoji} {priority}{due_display}')
        elif due_display:
            print(f'  {due_display}')
        print()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: notion_helper.py <command>")
        print("\nCommands:")
        print("  search-todo                    Search for Todo databases")
        print("  get-page <page_id>           Get a page")
        print("  get-db <database_id>            Get database schema")
        print("  query-db <database_id> [filter]  Query database (JSON)")
        print("  display-todo [db_id] [status] [limit]  Display todo list")
        print("    status_filter: completed, in-progress, next-up, end")
        print("    limit: max number of items to display")
        print("  todo [max_items]               Display top N todo items")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'search-todo':
        result = search_todo_lists()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif command == 'get-page':
        if len(sys.argv) < 3:
            print("Error: page_id required", file=sys.stderr)
            sys.exit(1)
        page_id = sys.argv[2]
        result = get_page(page_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif command == 'get-db':
        if len(sys.argv) < 3:
            print("Error: database_id required", file=sys.stderr)
            sys.exit(1)
        db_id = sys.argv[2]
        result = get_database(db_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif command == 'query-db':
        if len(sys.argv) < 3:
            print("Error: database_id required", file=sys.stderr)
            sys.exit(1)
        db_id = sys.argv[2]
        filter_json = sys.argv[3] if len(sys.argv) > 3 else None
        result = query_database(db_id, filter_json)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif command == 'display-todo':
        db_id = sys.argv[2] if len(sys.argv) > 2 else '1fbf82d039f880b19182cdb5ac44f31e'
        status_filter = sys.argv[3] if len(sys.argv) > 3 else None
        limit = int(sys.argv[4]) if len(sys.argv) > 4 else None
        display_todo_list(db_id, status_filter, limit)
    elif command == 'todo':
        # todo [max_items] - uses default database
        DEFAULT_DB = '1fbf82d039f880b19182cdb5ac44f31e'
        if len(sys.argv) > 2:
            # Check if arg is a number (max_items) or database ID
            arg = sys.argv[2]
            if arg.isdigit():
                max_items = int(arg)
                db_id = DEFAULT_DB
            else:
                db_id = arg
                max_items = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        else:
            db_id = DEFAULT_DB
            max_items = 10
        display_todo_simple(db_id, max_items)
    else:
        print(f"❌ Unknown command: {command}", file=sys.stderr)
        sys.exit(1)
