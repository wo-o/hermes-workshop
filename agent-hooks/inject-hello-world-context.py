#!/usr/bin/env python3
"""매 LLM 호출에 Hello World! 접두사 응답 지시를 추가한다."""

import json
import sys

json.load(sys.stdin)
print(json.dumps({"context": "응답 앞에 항상 Hello World!를 붙여줘"}, ensure_ascii=False))
