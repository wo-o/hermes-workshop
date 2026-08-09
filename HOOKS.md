# Hermes Hooks 실습

공식 문서: <https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks>

이 실습은 서로 다른 세 가지 Hook 시스템을 구분합니다.

| 종류 | 등록 위치 | 실행 범위 | `hermes hooks list` 표시 |
|---|---|---|---|
| Gateway Hook | `$HERMES_HOME/hooks/<name>/` | Gateway만 | 아니요 |
| Plugin Hook | `ctx.register_hook(...)` | CLI + Gateway | 아니요 (`hermes plugins list` 사용) |
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

## 2. 매 답변 앞에 `Hello World!` 추가

최종 답변을 확실하게 바꾸려면 이 리포지토리의 Plugin Hook을 사용합니다. 루트 플러그인은 `transform_llm_output`을 등록하고 `Hello World!`를 최종 응답 앞에 한 번만 추가합니다.

```bash
hermes plugins install wo-o/hermes-workshop --enable
hermes config set display.streaming false
hermes chat -q 'reply only with: OK' --quiet
```

예상 최종 출력:

```text
Hello World!
OK
```

스트리밍이 켜져 있으면 모델의 원래 응답 토큰이 먼저 보인 뒤 변환 결과가 다시 표시될 수 있습니다. 실습에서는 `display.streaming=false`로 최종 변환 결과만 확인합니다.

Plugin Hook은 다음 명령에 표시되지 않는 것이 정상입니다.

```bash
hermes hooks list
hermes hooks test transform_llm_output
```

`hermes hooks ...`는 설정 파일에 선언된 Shell Hook을 검사합니다. 설치된 Plugin Hook은 다음에서 플러그인의 Hook 개수로 확인합니다.

```bash
hermes plugins list
```

정리:

```bash
hermes plugins disable workshop-greeting
hermes plugins remove workshop-greeting
hermes config set display.streaming true
```

## 3. 왜 `transform_llm_output` Shell Hook으로 만들지 않았나

Hermes v0.20.0 및 2026-08-09 기준 최신 소스의 Shell Hook 응답 파서는 이벤트별 구조화 결과를 처리합니다. 예를 들어 `pre_tool_call`의 block 결정, `pre_verify`의 continue 결정, 여러 이벤트의 `context` 문자열을 Dispatcher 반환값으로 변환합니다.

반면 `transform_llm_output` 호출부는 Hook 반환값으로 Python `str`을 요구합니다. Shell Hook subprocess의 JSON 응답을 이 문자열로 변환하는 wire shape가 아직 구현되어 있지 않으므로 Shell Hook으로 최종 답변을 prepend하는 예제는 현재 실제로 동작하지 않습니다. `hermes hooks test transform_llm_output`에 Shell Hook을 억지로 등록하면 실행 자체는 되더라도 `parsed: <none>`이거나 최종 응답에 반영되지 않습니다.

따라서 이 저장소는 동작하지 않는 예제를 제공하는 대신, 같은 이벤트를 사용하는 Plugin Hook으로 검증 가능한 해결책을 제공합니다.

## 4. Shell Hook: 위험 명령 차단

교육용 `repo-guard.py`는 `terminal` 호출 중 `rm -rf`, `git reset --hard`, 강제 `git clean` 패턴을 차단합니다. 완전한 샌드박스가 아니라 실수 방지용 추가 방어선입니다.

```bash
mkdir -p "$HERMES_HOME/agent-hooks"
cp agent-hooks/repo-guard.py "$HERMES_HOME/agent-hooks/"
chmod +x "$HERMES_HOME/agent-hooks/repo-guard.py"
hermes config edit
```

편집기에서 기존 설정을 보존한 채 다음 항목을 `hooks:` 아래에 병합합니다.

```yaml
hooks:
  pre_tool_call:
    - matcher: terminal
      command: /absolute/path/to/HERMES_HOME/agent-hooks/repo-guard.py
      timeout: 5
```

`hermes config set`은 현재 JSON 배열 문자열을 YAML list로 변환하지 않습니다. `hooks.pre_tool_call` 전체를 JSON 문자열로 설정하면 Hook이 등록되지 않으므로 이 구조에는 `hermes config edit`을 사용합니다.

`command`에는 `printf '%s\n' "$HERMES_HOME"`으로 확인한 실제 절대 경로를 넣으세요. Shell Hook 명령은 shell 없이 실행되므로 YAML의 `$HERMES_HOME`이나 `~`가 자동 확장된다고 가정하지 않습니다.

설정 저장 직후 구조를 검사합니다.

```bash
hermes config check
```

중요: Hermes v0.20.0의 Shell Hook에는 `fail_closed` 설정이 없습니다. 실행 파일 누락, timeout, 잘못된 출력 등으로 Hook이 실패하면 terminal 호출을 자동으로 차단하지 않습니다. 따라서 `repo-guard`를 보안 게이트로 사용하면 안 됩니다.

처음 등록할 때는 대화형 승인을 받거나 명시적으로 승인합니다.

```bash
hermes --accept-hooks chat -q 'reply only with: hook approved' --quiet
```

점검과 안전한 합성 테스트:

```bash
hermes hooks list
hermes hooks test pre_tool_call --for-tool terminal \
  --payload-file examples/payloads/dangerous-terminal.json
hermes hooks doctor
```

승인 기록은 `$HERMES_HOME/shell-hooks-allowlist.json`에 저장됩니다. 파일을 직접 편집하기보다 최초 승인 또는 `--accept-hooks`를 사용하고 `hermes hooks list`로 상태를 확인하세요.

정리:

```bash
hermes hooks revoke "$HERMES_HOME/agent-hooks/repo-guard.py"
hermes config unset hooks.pre_tool_call
rm "$HERMES_HOME/agent-hooks/repo-guard.py"
```

## 5. Shell Hook: Git 상태 컨텍스트 주입

`pre_llm_call`은 Claude Code의 `UserPromptSubmit`에 가까운 위치에서 실행됩니다. 다음 예제는 현재 작업 디렉터리가 Git 저장소일 때 `git status --short --branch`를 매 턴의 임시 사용자 컨텍스트에 추가합니다. 출력은 최대 100줄·8,000자로 제한합니다.

```bash
cp agent-hooks/inject-git-status.py "$HERMES_HOME/agent-hooks/"
chmod +x "$HERMES_HOME/agent-hooks/inject-git-status.py"
hermes config edit
```

편집기에서 기존 `hooks:` 매핑에 다음 이벤트를 병합합니다.

```yaml
hooks:
  pre_llm_call:
    - command: /absolute/path/to/HERMES_HOME/agent-hooks/inject-git-status.py
      timeout: 5
```

설정을 저장한 뒤 최초 승인을 포함해 실행합니다.

```bash
hermes --accept-hooks chat -q '현재 Git 상태를 한 줄로 설명해줘' --quiet
```

검증:

```bash
hermes hooks list
hermes hooks test pre_llm_call
hermes hooks doctor
```

정리:

```bash
hermes hooks revoke "$HERMES_HOME/agent-hooks/inject-git-status.py"
hermes config unset hooks.pre_llm_call
rm "$HERMES_HOME/agent-hooks/inject-git-status.py"
```

## 보안 경계

- Gateway Hook과 Plugin Hook은 Hermes 프로세스 안에서 Python을 실행합니다.
- Shell Hook은 별도 프로세스지만 현재 사용자 권한과 자격 증명에 접근할 수 있습니다.
- 공개 Hook이나 Plugin을 활성화하기 전에 `HOOK.yaml`, `handler.py`, `plugin.yaml`, `__init__.py`, 실행 스크립트를 검토하세요.
- Secret 값이나 전체 명령 인자를 로그에 남기지 마세요.
- `repo-guard`는 패턴 기반 보조 장치이며 OS 권한, 승인 정책, 격리 환경을 대체하지 않습니다.
- Git 브랜치명과 파일명도 공격자가 제어할 수 있는 입력입니다. `inject-git-status.py`는 이를 명시적으로 신뢰할 수 없는 JSON 데이터로 표시하지만, 민감한 저장소에서는 Hook을 활성화하기 전에 출력 범위와 신뢰 경계를 다시 검토하세요.
