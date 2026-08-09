"""데모 Hermes 플러그인이 노출하는 도구 스키마."""

COURSE_GREETING = {
    "name": "course_greeting",
    "description": (
        "설치된 플러그인 버전이 포함된 고정 형식의 Hermes 워크숍 인사말을 "
        "반환합니다. 이 데모 플러그인 설치를 검증할 때 사용하세요."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "인사할 사람의 이름.",
            }
        },
        "required": ["name"],
    },
}
