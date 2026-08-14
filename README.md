# Hermes Workshop

하나의 업스트림 Git 리포지토리에서 Hermes의 Profile distribution, 스킬, 이벤트 훅 확장 경로를 시연하는 재사용 가능한 교육용 리포지토리입니다. 의존성을 최소화했습니다.

1. `distribution.yaml`, `SOUL.md` — 한 명령으로 설치·업데이트하는 교육용 Profile
2. `skills/` — 설치·업데이트를 시연하는 `hello` 스킬
3. `hooks/`, `agent-hooks/` — Gateway Hook과 Shell Hook 실습 예제

각 컴포넌트는 눈에 보이는 버전과 색상 마커를 일부러 반환합니다. 업스트림 업데이트가 각 설치 경로에 실제로 반영됐는지 수업에서 직접 확인하기 위해서입니다.

## 요구 사항

- Hermes Agent v0.20.0 이상
- Git

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

## 스킬

기본 설치·업데이트 시연은 `hello` 스킬을 사용합니다.

```bash
hermes skills inspect wo-o/hermes-workshop/skills/hello
hermes skills install wo-o/hermes-workshop/skills/hello --yes
hermes skills check hello
hermes skills update hello
```

새 세션을 시작하거나 `/reload-skills`를 실행한 뒤 `/hello Techwoo`를 호출하세요.

## Event Hooks

Gateway 재시작 로그와 Shell Hook 승인·검증 실습은 [HOOKS.md](HOOKS.md)를 따르세요.

```bash
hermes hooks list
hermes hooks doctor
```

## 정리

```bash
hermes skills uninstall hello
```

Hook별 설치와 정리 명령은 [HOOKS.md](HOOKS.md)에 있습니다.

## 보안 경계

각 방식은 신뢰 모델이 서로 다릅니다. 스킬은 지시문을 제공하고, Gateway Hook은 Hermes 프로세스 안에서 Python을 실행합니다. Shell Hook은 별도 프로세스에서 현재 사용자 권한으로 실행됩니다. 어떤 것이든 활성화하기 전에 공개 소스를 먼저 검토하세요.

라이선스: MIT
