"""데모 Hermes 플러그인의 도구 핸들러."""

import json

VERSION = "0.3.1"
COLOR = "green"


def course_greeting(args, **kwargs) -> str:
    """예외를 밖으로 흘리지 않고 항상 안정적인 JSON 응답을 반환한다."""
    del kwargs
    try:
        name = str(args.get("name", "")).strip()
        if not name:
            return json.dumps({"error": "name이 필요합니다"}, ensure_ascii=False)
        return json.dumps(
            {
                "component": "plugin",
                "version": VERSION,
                "color": COLOR,
                "message": f"안녕하세요, {name}님! Hermes 워크숍이 준비되었습니다.",
            },
            ensure_ascii=False,
        )
    except Exception as exc:
        return json.dumps({"error": f"course greeting 실패: {exc}"}, ensure_ascii=False)
