#!/usr/bin/env python3
"""현재 Git 변경 요약을 매 턴의 임시 사용자 컨텍스트에 추가한다."""

import json
import subprocess
import sys


def main() -> int:
    payload = json.load(sys.stdin)
    cwd = payload.get("cwd") or "."
    result = subprocess.run(
        ["git", "status", "--short", "--branch"],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=3,
        check=False,
    )
    if result.returncode != 0:
        print("{}")
        return 0

    status = result.stdout.strip()
    if not status:
        print("{}")
        return 0

    print(
        json.dumps(
            {"context": f"현재 작업 디렉터리의 git status:\n{status}"},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
