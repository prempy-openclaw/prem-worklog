#!/usr/bin/env python3
import sys
import yaml
from pathlib import Path

REQUIRED = [
    "task_id",
    "owner",
    "input_summary",
    "output_summary",
    "artifacts",
    "verification",
    "risks",
    "next_handoff_to",
    "status",
]
ALLOWED_STATUS = {"done", "blocked", "needs_review"}


def validate(path: Path):
    data = yaml.safe_load(path.read_text())
    missing = [k for k in REQUIRED if k not in data]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"

    if data["status"] not in ALLOWED_STATUS:
        return False, f"Invalid status: {data['status']}"

    if not isinstance(data.get("verification"), list) or len(data["verification"]) == 0:
        return False, "verification must be a non-empty list"

    if data["status"] == "blocked":
        risks = data.get("risks", [])
        has_unblock = any("unblock" in str(r).lower() for r in risks)
        if not has_unblock:
            return False, "blocked status requires an explicit unblock condition in risks"

    return True, "OK"


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_handoff.py <handoff.yaml>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: file not found: {path}")
        sys.exit(1)

    ok, msg = validate(path)
    if ok:
        print(f"PASS: {path} -> {msg}")
        sys.exit(0)
    else:
        print(f"FAIL: {path} -> {msg}")
        sys.exit(2)


if __name__ == "__main__":
    main()
