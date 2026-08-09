"""Hermes 플러그인 훅 예제."""


def prefix_hello_world(response_text: str, **_kwargs) -> str:
    """최종 답변 앞에 고정된 인사말을 한 번 추가한다."""
    prefix = "Hello World!"
    if response_text == prefix or response_text.startswith(f"{prefix}\n"):
        return response_text
    return f"{prefix}\n{response_text}"
