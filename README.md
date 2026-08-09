# Hermes Workshop

하나의 업스트림 Git 리포지토리에서 Hermes의 Profile distribution, Kanban, 스킬, 플러그인, MCP, 이벤트 훅 확장 경로를 시연하는 재사용 가능한 교육용 리포지토리입니다. 의존성을 최소화했습니다.

1. `distribution.yaml`, `SOUL.md` — 한 명령으로 설치·업데이트하는 교육용 Profile
2. `skills/` — 설치 가능한 Hermes 스킬과 단계별 교육 예제
3. 리포지토리 루트 — `course_greeting` 도구와 `transform_llm_output` Hook을 제공하는 네이티브 Hermes 플러그인
4. `hermes-workshop-mcp` — `lab_status` 도구를 제공하는 stdio MCP 서버
5. `hooks/`, `agent-hooks/` — Gateway Hook과 Shell Hook 실습 예제

각 컴포넌트는 눈에 보이는 버전과 색상 마커를 일부러 반환합니다. 업스트림 업데이트가 각 설치 경로에 실제로 반영됐는지 수업에서 직접 확인하기 위해서입니다.

## 요구 사항

- Hermes Agent v0.20.0 이상
- Git
- MCP 실행용 `uv`

## Profile distribution

전체 교육용 Profile과 저장소의 스킬을 한 번에 설치합니다. API 키, 인증 정보, memory, session은 distribution에 포함되지 않습니다.

```bash
hermes profile install https://github.com/wo-o/hermes-workshop.git --alias
hermes profile info hermes-workshop
hermes profile show hermes-workshop
```

별칭을 만들었다면 `hermes-workshop`으로, 별칭 없이 설치했다면 `hermes -p hermes-workshop`으로 실행합니다. 저장소가 업데이트된 뒤에는 다음 명령으로 배포판 소유 파일을 갱신합니다.

```bash
hermes profile update hermes-workshop
```

이미 같은 이름의 로컬 Profile이 있으면 덮어쓰지 말고 시험용 이름을 지정합니다.

```bash
hermes profile install https://github.com/wo-o/hermes-workshop.git \
  --name hermes-workshop-test
```

> 이 저장소는 현재 비공개이므로 설치하는 Git 환경에 `wo-o/hermes-workshop` 읽기 권한이 필요합니다.

## Kanban 다중 Profile 실습

`kanban-service-planning` 스킬은 인프라 계획과 운영 계획을 병렬로 실행하고, 두 결과에 의존하는 최종 출시 체크리스트를 작성하는 실습입니다. 실제 클라우드나 서버는 생성하지 않습니다.

Profile distribution으로 설치한 뒤 `hermes-workshop` Profile에게 “Kanban 신규 서비스 출시 계획 실습을 진행해 줘”라고 요청하거나, 전체 명령을 직접 따라 합니다.

- [Kanban 실습 전체 가이드](skills/kanban-service-planning/references/lab.md)
- [Kanban 실행 스킬](skills/kanban-service-planning/SKILL.md)

## 스킬

기본 설치·업데이트 시연은 `lab-release-check`를 사용합니다.

```bash
hermes skills inspect wo-o/hermes-workshop/skills/lab-release-check
hermes skills install wo-o/hermes-workshop/skills/lab-release-check --yes
hermes skills check lab-release-check
hermes skills update lab-release-check
```

새 세션을 시작하거나 `/reload-skills`를 실행한 뒤 `/lab-release-check Techwoo`를 호출하세요.

회의록 정리, 체계적 디버깅, TDD, GitHub 이슈 작성, README 검증 실습은 [SKILLS.md](SKILLS.md)를 따르세요. 각 스킬에는 그대로 사용할 수 있는 샘플 입력과 관찰 포인트가 포함되어 있습니다.

## 네이티브 플러그인

```bash
hermes plugins install wo-o/hermes-workshop --enable
hermes plugins list --user
hermes plugins update workshop-greeting
```

설치나 업데이트 후에는 Hermes CLI 또는 게이트웨이를 재시작하세요. Hermes에게 `Techwoo`를 대상으로 `course_greeting`을 호출해 달라고 요청하면 됩니다.

이 플러그인은 `transform_llm_output` Plugin Hook도 등록하여 최종 답변 앞에 `Hello World!`를 붙입니다. Plugin Hook은 `hermes hooks list`에 표시되지 않습니다.

## Event Hooks

Gateway 재시작 로그, 최종 답변 변환, Shell Hook 승인·검증, 위험 명령 차단 및 Git 상태 주입 실습은 [HOOKS.md](HOOKS.md)를 따르세요.

```bash
hermes hooks list
hermes hooks doctor
```

## MCP 서버

Git 리포지토리를 stdio 런처로 등록합니다. `--refresh` 옵션을 주면 MCP 프로세스가 시작될 때 `uvx`가 브랜치를 다시 확인합니다. 비공개 저장소라면 실행 환경에도 해당 저장소를 읽을 GitHub 인증이 필요합니다.

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

Hook별 설치와 정리 명령은 [HOOKS.md](HOOKS.md)에 있습니다.

## 보안 경계

각 방식은 신뢰 모델이 서로 다릅니다. 스킬은 지시문을 제공하고, 네이티브 플러그인과 Gateway Hook은 Hermes 프로세스 안에서 Python을 실행합니다. Shell Hook은 별도 프로세스에서 현재 사용자 권한으로 실행되며, MCP 서버는 MCP로 연결된 별도 프로세스로 실행됩니다. 어떤 것이든 활성화하기 전에 공개 소스를 먼저 검토하세요.

라이선스: MIT
