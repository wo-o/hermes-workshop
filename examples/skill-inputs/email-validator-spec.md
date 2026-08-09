# 이메일 검증 요구사항

`is_valid_email(value)` 함수를 구현합니다.

- 문자열 하나를 입력받습니다.
- 앞뒤 공백은 무시합니다.
- `@`가 정확히 하나 있어야 합니다.
- 로컬 부분과 도메인 부분은 비어 있으면 안 됩니다.
- 도메인에는 점(`.`)이 하나 이상 있어야 합니다.
- 공백이 포함된 주소는 거부합니다.
- 잘못된 입력에는 예외 대신 `False`를 반환합니다.

예시:

| 입력 | 결과 |
|---|---|
| `user@example.com` | `True` |
| ` user@example.com ` | `True` |
| `user@example` | `False` |
| `@example.com` | `False` |
| `user name@example.com` | `False` |
| `None` | `False` |
