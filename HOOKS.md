# Hermes Hooks 실습

공식 문서: <https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks>

이 실습은 서로 다른 두 가지 Hook 시스템을 구분합니다.

| 종류 | 등록 위치 | 실행 범위 | `hermes hooks list` 표시 |
|---|---|---|---|
| Gateway Hook | `$HERMES_HOME/hooks/<name>/` | Gateway만 | 아니요 |
| Shell Hook | `config.yaml`의 `hooks:` | CLI + Gateway | 예 |

`hermes hooks list`는 Shell Hook과 Outbound Webhook을 표시하고, `test`와 `doctor`는 Shell Hook을 검사합니다. 이름이 비슷하지만 Gateway Hook이나 Plugin Hook의 전체 목록을 보여주는 명령은 아닙니다.

아래 명령은 활성 프로필의 Hermes 홈을 사용합니다. 별도 프로필을 사용한다면 그 프로필을 가리키도록 `HERMES_HOME`을 먼저 설정하세요.

```bash
export HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
printf 'Hermes home: %s\n' "$HERMES_HOME"
```

## 1. Gateway 재시작 로그

리포지토리의 예제를 사용자 Hook 디렉터리에 설치합니다.

```bash
mkdir -p "$HERMES_HOME/hooks"
cp -R hooks/hello-world-restart "$HERMES_HOME/hooks/"
```

최종 파일은 다음 두 개입니다.

```text
$HERMES_HOME/hooks/hello-world-restart/HOOK.yaml
$HERMES_HOME/hooks/hello-world-restart/handler.py
```

Hermes 통합 로그를 별도 터미널에서 확인한 뒤 재시작합니다.

```bash
hermes logs -f
```

```bash
hermes gateway restart
```

재시작 후 `agent.log`에서 `hooks.hello-world-restart: Hello World!`를 확인하세요. `hermes logs gateway -f`에서는 Gateway 프로세스의 시작과 Hook 로드 메시지를 확인할 수 있지만, 이 Handler의 Python logger 출력은 통합 `agent.log`에 기록됩니다.

정리:

```bash
rm -r "$HERMES_HOME/hooks/hello-world-restart"
hermes gateway restart
```

## 2. Shell Hook: `Hello World!` 응답 지시 주입

`pre_llm_call` Shell Hook의 `context`는 해당 호출의 임시 사용자 컨텍스트에 추가됩니다. 다음 예제는 모델에게 모든 응답의 첫 줄에 `Hello World!`를 붙이도록 지시합니다.

```bash
cp agent-hooks/inject-hello-world-context.py "$HERMES_HOME/agent-hooks/"
chmod +x "$HERMES_HOME/agent-hooks/inject-hello-world-context.py"
hermes config edit
```

기존 `hooks:` 매핑에 다음 이벤트를 병합합니다.

```yaml
hooks:
  pre_llm_call:
    - command: /absolute/path/to/HERMES_HOME/agent-hooks/inject-hello-world-context.py
      timeout: 5
```

설정을 저장한 뒤 최초 승인을 포함해 실행합니다.

```bash
hermes --accept-hooks chat -q 'OK만 답해줘' --quiet
```

이 방식은 모델에 보내는 지시이므로 모델이 반드시 따르는 출력 변환을 보장하지는 않습니다. Hermes v0.20.0의 Shell Hook은 `transform_llm_output`처럼 최종 응답 문자열을 결정적으로 교체하는 wire shape를 아직 제공하지 않으므로, 이 실습은 모델 지시 주입까지만 다룹니다.

검증과 정리:

```bash
hermes hooks test pre_llm_call
hermes hooks doctor
hermes hooks revoke "$HERMES_HOME/agent-hooks/inject-hello-world-context.py"
hermes config unset hooks.pre_llm_call
rm "$HERMES_HOME/agent-hooks/inject-hello-world-context.py"
```

## 보안 경계

- Gateway Hook은 Hermes 프로세스 안에서 Python을 실행합니다.
- Shell Hook은 별도 프로세스지만 현재 사용자 권한과 자격 증명에 접근할 수 있습니다.
- 공개 Hook을 활성화하기 전에 `HOOK.yaml`, `handler.py`, 실행 스크립트를 검토하세요.
- Secret 값이나 전체 명령 인자를 로그에 남기지 마세요.
