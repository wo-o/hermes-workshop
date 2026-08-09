#!/usr/bin/env python3
"""위험도가 높은 터미널 명령을 보수적으로 차단하는 교육용 Shell Hook."""

import json
import re
import sys

BLOCKED_PATTERNS = (
    (re.compile(r"(^|[;&|]\s*)rm\s+-(?:[^\s]*r[^\s]*f|[^\s]*f[^\s]*r)\b"), "recursive forced rm"),
    (re.compile(r"\bgit\s+reset\s+--hard\b"), "git reset --hard"),
    (re.compile(r"\bgit\s+clean\s+-[^\s]*f"), "git clean with force"),
)


def main() -> int:
    payload = json.load(sys.stdin)
    tool_input = payload.get("tool_input") or {}
    command = tool_input.get("command", "")

    if not isinstance(command, str):
        print("{}")
        return 0

    for pattern, label in BLOCKED_PATTERNS:
        if pattern.search(command):
            print(
                json.dumps(
                    {
                        "action": "block",
                        "message": f"repo-guard가 위험 명령을 차단했습니다: {label}",
                    },
                    ensure_ascii=False,
                )
            )
            return 0

    print("{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
