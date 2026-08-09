# Hermes Workshop

하나의 업스트림 Git 리포지토리에서 세 가지 Hermes 확장 경로를 시연하는 공개 교육용 리포지토리입니다. 의존성을 최소화했습니다.

1. `skills/lab-release-check` — 설치 가능한 Hermes 스킬
2. 리포지토리 루트 — `course_greeting` 도구를 제공하는 네이티브 Hermes 플러그인
3. `hermes-workshop-mcp` — `lab_status` 도구를 제공하는 stdio MCP 서버

세 컴포넌트는 눈에 보이는 버전과 색상 마커를 일부러 반환합니다. 업스트림 업데이트가 각 설치 경로에 실제로 반영됐는지 수업에서 직접 확인하기 위해서입니다.

## 요구 사항

- Hermes Agent v0.20.0 이상
- Git
- MCP 실행용 `uv`

## 스킬

```bash
hermes skills inspect wo-o/hermes-workshop/skills/lab-release-check
hermes skills install wo-o/hermes-workshop/skills/lab-release-check --yes
hermes skills check lab-release-check
hermes skills update lab-release-check
```

새 세션을 시작하거나 `/reload-skills`를 실행한 뒤 `/lab-release-check Techwoo`를 호출하세요.

## 네이티브 플러그인

```bash
hermes plugins install wo-o/hermes-workshop --enable
hermes plugins list --user
hermes plugins update workshop-greeting
```

설치나 업데이트 후에는 Hermes CLI 또는 게이트웨이를 재시작하세요. Hermes에게 `Techwoo`를 대상으로 `course_greeting`을 호출해 달라고 요청하면 됩니다.

## MCP 서버

공개 Git 리포지토리를 stdio 런처로 등록합니다. `--refresh` 옵션을 주면 MCP 프로세스가 시작될 때 `uvx`가 브랜치를 다시 확인합니다.

```bash
hermes mcp add workshop_lab --command uvx --connect-timeout 120 \
  --args --refresh --from git+https://github.com/wo-o/hermes-workshop.git \
  hermes-workshop-mcp
hermes mcp test workshop_lab
```

업스트림이 업데이트되면 `hermes mcp test workshop_lab`을 다시 실행하고, 활성 세션에서 `/reload-mcp`로 MCP 도구를 다시 불러오세요.

## 로컬 검증

```bash
uv run --with pytest pytest -q
uv build
```

## 정리

```bash
hermes skills uninstall lab-release-check
hermes plugins disable workshop-greeting
hermes plugins remove workshop-greeting
hermes mcp remove workshop_lab
```

## 보안 경계

세 가지 방식은 신뢰 모델이 서로 다릅니다. 스킬은 지시문을 제공하고, 네이티브 플러그인은 Hermes 프로세스 안에서 Python을 실행하며, MCP 서버는 MCP로 연결된 별도 프로세스로 실행됩니다. 어떤 것이든 활성화하기 전에 공개 소스를 먼저 검토하세요.

라이선스: MIT
