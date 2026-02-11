#!/usr/bin/env python3
import sys
import yaml
from pathlib import Path

STATE = Path('/root/.openclaw/workspace/agent-teams/incident_mode.yaml')


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ('on', 'off', 'status'):
        print('Usage: incident_mode.py <on|off|status> [reason]')
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == 'status':
        if not STATE.exists():
            print('incident_mode: off')
            return
        data = yaml.safe_load(STATE.read_text()) or {}
        print(f"incident_mode: {'on' if data.get('enabled') else 'off'} | reason: {data.get('reason','-')}")
        return

    if cmd == 'on':
        reason = sys.argv[2] if len(sys.argv) > 2 else 'unspecified'
        data = {'enabled': True, 'reason': reason}
        STATE.write_text(yaml.safe_dump(data, sort_keys=False))
        print(f'PASS: incident mode ON ({reason})')
    else:
        STATE.write_text(yaml.safe_dump({'enabled': False, 'reason': ''}, sort_keys=False))
        print('PASS: incident mode OFF')


if __name__ == '__main__':
    main()
