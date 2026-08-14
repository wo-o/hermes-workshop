# 스킬 교육 실습

이 폴더에는 같은 요청을 일관된 절차와 품질 기준으로 처리하는 교육용 스킬 7개가 있습니다.

| 스킬 | 핵심 행동 | 추천 대상 |
|---|---|---|
| `lab-release-check` | 설치·업데이트 버전 확인 | 설치 입문 |
| `hello` | 이름을 받아 정해진 형식의 인사말 출력 | 스킬 입문 |
| `meeting-action-items` | 회의록에서 근거 있는 실행 항목 추출 | 전 직군 |
| `systematic-bug-fix` | 재현 → 원인 → 회귀 테스트 → 수정 | 개발자 |
| `tdd-feature-workflow` | RED → GREEN → REFACTOR | 개발자 |
| `github-issue-spec` | 요청을 검증 가능한 이슈로 구조화 | 개발·기획 |
| `verified-readme` | 문서 명령을 실제 프로젝트와 대조 | 개발·DevRel |

## 1. 설치

먼저 내용을 검사한 뒤 필요한 스킬만 설치합니다.

```bash
hermes skills inspect wo-o/hermes-workshop/skills/meeting-action-items
hermes skills install wo-o/hermes-workshop/skills/hello --yes
hermes skills install wo-o/hermes-workshop/skills/meeting-action-items --yes
hermes skills install wo-o/hermes-workshop/skills/systematic-bug-fix --yes
hermes skills install wo-o/hermes-workshop/skills/tdd-feature-workflow --yes
hermes skills install wo-o/hermes-workshop/skills/github-issue-spec --yes
hermes skills install wo-o/hermes-workshop/skills/verified-readme --yes
```

설치 후 새 세션을 시작하거나 `/reload-skills`를 실행합니다.

```bash
hermes skills check hello
hermes skills check meeting-action-items
hermes skills check systematic-bug-fix
hermes skills check tdd-feature-workflow
hermes skills check github-issue-spec
hermes skills check verified-readme
```

## 2. 시연 순서

### A. 비개발자: 회의록 정리

```text
meeting-action-items 스킬을 사용해서
examples/skill-inputs/meeting-notes.md를 정리해줘.
```

관찰할 점:

- 확정된 결정과 제안을 구분하는가
- 없는 담당자나 기한을 추측하지 않는가
- 각 항목에 원문 근거가 있는가

### B. 입문: 정해진 인사말

```text
hello 스킬을 사용해서 Techwoo에게 인사해줘.
```

관찰할 점:

- `안녕하세요, Techwoo님!` 한 줄만 출력하는가
- 이름이 없을 때만 이름을 물어보는가

### C. 개발자: 버그 수정

```text
systematic-bug-fix 스킬을 사용해서
examples/skill-lab/discount.py의 버그를 재현하고 수정해줘.
테스트는 examples/skill-lab/test_discount.py에 있어.
```

관찰할 점:

- 코드를 먼저 바꾸지 않고 실패를 재현하는가
- 테스트가 실패한 실제 이유를 확인하는가
- 수정 후 관련 테스트를 다시 실행하는가

원상 복구:

```bash
git restore examples/skill-lab/discount.py
```

### D. 개발자: TDD

```text
tdd-feature-workflow 스킬을 사용해서
examples/skill-inputs/email-validator-spec.md 요구사항을
examples/skill-lab/email_validator.py에 구현해줘.
```

관찰할 점:

- 구현 전에 실패 테스트를 만드는가
- RED와 GREEN을 실제 실행 결과로 확인하는가
- 경계값을 추가하는가

원상 복구:

```bash
git restore examples/skill-lab/email_validator.py
git clean -f examples/skill-lab/test_email_validator.py
```

### E. 협업: GitHub 이슈 초안

```text
github-issue-spec 스킬을 사용해서
examples/skill-inputs/issue-request.md를 GitHub 이슈 초안으로 바꿔줘.
실제 이슈는 생성하지 마.
```

관찰할 점:

- 완료 조건이 객관적으로 검증 가능한가
- 확인하지 않은 파일명이나 담당자를 만들지 않는가
- 초안 요청인데 외부 쓰기 작업을 하지 않는가

### F. 문서: README 검증

```text
verified-readme 스킬을 사용해서
examples/skill-inputs/README.bad.md의 문제를 찾아줘.
아직 파일은 수정하지 마.
```

관찰할 점:

- 매니페스트와 실제 명령을 대조하는가
- secret 예시와 검증 없는 성공 주장을 찾는가
- 요청하지 않은 수정은 하지 않는가

## 3. 개념 정리

```text
프롬프트: 이번 작업의 목적과 범위
스킬: 반복 가능한 절차와 품질 기준
도구: 파일·터미널·웹을 실제 조작
MCP: GitHub 같은 외부 시스템의 도구를 연결
```

스킬 전후를 비교하려면 같은 입력을 새 세션에서 한 번은 스킬 없이, 한 번은 스킬을 명시해 실행합니다. 결과 문장보다 작업 순서, 근거, 검증 여부를 비교하세요.

## 4. 제거

```bash
hermes skills uninstall meeting-action-items
hermes skills uninstall hello
hermes skills uninstall systematic-bug-fix
hermes skills uninstall tdd-feature-workflow
hermes skills uninstall github-issue-spec
hermes skills uninstall verified-readme
```
