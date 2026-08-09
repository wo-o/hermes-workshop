# Kanban 실습: 신규 웹 서비스 출시 계획

## 목표와 안전 범위

세 개의 Hermes Profile이 인프라 계획, 운영 계획, 최종 출시 체크리스트를 협업해 작성한다. 실제 클라우드·서버·모니터링 시스템은 생성하거나 조회하지 않는다.

```text
[인프라 계획] ──┐
                ├──> [최종 출시 계획]
[운영 계획] ────┘
```

대상은 사내 직원 100명이 사용하는 간단한 업무 요청 웹 서비스다. 웹 애플리케이션과 데이터베이스가 필요하지만 제품과 공급자는 아직 정하지 않았다.

## 0. 사전 확인

```bash
hermes --version
hermes profile create --help
hermes kanban create --help
hermes kanban boards create --help
hermes gateway status
```

이 가이드는 Hermes Agent v0.20.0 이상을 기준으로 한다. 기존에 같은 이름의 Profile이나 보드가 있으면 덮어쓰거나 삭제하지 말고 별도 이름을 사용한다.

## 1. 역할별 Profile 생성

현재 `default` Profile의 모델과 인증 설정을 복제한다.

```bash
hermes profile create infra-planner \
  --clone-from default \
  --description "신규 서비스의 서버, 네트워크, 데이터베이스와 환경 구성을 계획한다."

hermes profile create ops-planner \
  --clone-from default \
  --description "신규 서비스의 모니터링, 백업, 장애 대응과 운영 기준을 계획한다."

hermes profile create plan-reviewer \
  --clone-from default \
  --description "인프라와 운영 계획을 검토하고 최종 출시 체크리스트로 통합한다."

hermes profile list
hermes kanban assignees
```

## 2. 전용 보드 생성

```bash
hermes kanban init
hermes kanban boards create service-plan-lab \
  --name "신규 서비스 계획 실습" \
  --description "간단한 신규 웹 서비스 출시 계획" \
  --switch
hermes kanban boards show
```

## 3. Gateway 준비

Kanban dispatcher는 Gateway 안에서 배정된 Profile worker를 실행한다. 각 Profile의 Gateway를 따로 시작하지 않는다.

```bash
hermes gateway start
hermes gateway status
```

실습 전에 Gateway가 이미 실행 중이었다면 정리 단계에서 중지하지 않는다.

## 4. 인프라 계획 카드

```bash
hermes kanban create "신규 웹 서비스 인프라 계획" \
  --assignee infra-planner \
  --priority 10 \
  --max-runtime 15m \
  --body "
사내 직원 100명이 사용하는 간단한 업무 요청 웹 서비스의 인프라 계획을 작성한다.

조건:
- 웹 애플리케이션과 데이터베이스가 필요하다.
- 개발 환경과 운영 환경을 구분한다.
- 실제 클라우드나 서버는 생성하지 않는다.
- 특정 제품이 미정이면 임의로 확정하지 않는다.

결과에 포함할 내용:
1. 필요한 인프라 구성요소
2. 개발 환경과 운영 환경 구성
3. 네트워크와 접근 제어
4. 데이터 저장과 백업 고려사항
5. 출시 전 준비 작업 5개
"
```

출력된 실제 ID를 기록한다.

```text
INFRA_ID=<실제 task ID>
```

## 5. 운영 계획 카드

```bash
hermes kanban create "신규 웹 서비스 운영 계획" \
  --assignee ops-planner \
  --priority 10 \
  --max-runtime 15m \
  --body "
사내 직원 100명이 사용하는 업무 요청 웹 서비스의 운영 계획을 작성한다.

조건:
- 전담 24시간 운영 인력은 없다.
- 실제 서버나 모니터링 시스템은 조회하지 않는다.
- 구축 결과가 아니라 앞으로 준비해야 할 계획을 작성한다.

결과에 포함할 내용:
1. 확인해야 할 서비스 지표
2. 필요한 모니터링과 알림
3. 백업 및 복구 기준
4. 장애 발생 시 대응 순서
5. 출시 전 준비 작업 5개
"
```

출력된 실제 ID를 기록한다.

```text
OPS_ID=<실제 task ID>
```

## 6. 의존성이 있는 최종 계획 카드

아래 자리표시자를 앞에서 받은 실제 ID로 교체한다.

```bash
hermes kanban create "신규 웹 서비스 최종 출시 계획" \
  --assignee plan-reviewer \
  --priority 20 \
  --parent <INFRA_ID> \
  --parent <OPS_ID> \
  --max-runtime 15m \
  --body "
인프라 계획과 운영 계획을 검토하고 하나의 신규 서비스 출시 계획으로 통합한다.

결과 형식:
1. 서비스 개요
2. 필요한 인프라
3. 운영 준비 항목
4. 우선순위가 있는 출시 체크리스트
5. 담당자와 선행 조건
6. 미결정 사항
7. 출시 가능 여부 판단 기준

실제 구축이 완료됐다고 표현하지 않는다.
각 항목을 필수, 권장, 추후 개선으로 구분한다.
"
```

출력된 실제 ID를 `FINAL_ID`로 기록한다. 이 시점에는 두 계획 카드가 `ready`, 최종 카드는 parent가 열려 있으므로 `todo`여야 한다.

```bash
hermes kanban list
hermes kanban stats
hermes kanban show <INFRA_ID>
hermes kanban show <OPS_ID>
hermes kanban show <FINAL_ID>
```

## 7. 병렬 실행과 상태 관찰

```bash
hermes kanban dispatch --dry-run
hermes kanban dispatch --max 2
hermes kanban list
hermes kanban stats
hermes kanban watch
```

`watch`는 `Ctrl+C`로 종료한다. 정상적인 변화는 다음과 같다.

```text
인프라 계획: ready → running → done
운영 계획:   ready → running → done
최종 계획:   todo → ready → running → done
```

두 parent가 완료됐지만 최종 카드가 즉시 실행되지 않으면 한 번 더 배차한다.

```bash
hermes kanban dispatch
```

## 8. 결과 검증

```bash
hermes kanban list
hermes kanban stats
hermes kanban show <FINAL_ID>
hermes kanban runs <FINAL_ID>
hermes kanban log <FINAL_ID> --tail 10000
```

최종 결과에 다음이 있어야 한다.

- 필요한 인프라 구성요소
- 개발 환경과 운영 환경 구분
- 모니터링·알림·백업·복구 계획
- 우선순위가 있는 출시 체크리스트
- 담당자와 선행 조건
- 미결정 사항
- 출시 가능 여부 판단 기준

## 9. 선택 실습: 사람의 조건 보충

운영 계획 카드가 완료되기 전에 수행한다.

```bash
hermes kanban block <OPS_ID> \
  "백업 보존 기간이 결정되지 않음" \
  --kind needs_input

hermes kanban comment <OPS_ID> \
  "백업은 7일간 보존하고 복구 목표 시간은 4시간으로 계획한다."

hermes kanban unblock <OPS_ID> \
  --reason "백업 조건 보충 완료"

hermes kanban dispatch
```

## 10. 진단과 복구

```bash
hermes kanban show <task-id>
hermes kanban context <task-id>
hermes kanban runs <task-id>
hermes kanban log <task-id> --tail 10000
hermes kanban diagnostics --task <task-id>
```

Worker가 중단되고 claim만 남았다면 기록을 확인한 후 reclaim한다.

```bash
hermes kanban reclaim <task-id> \
  --reason "진행 기록이 없어 재배차"
hermes kanban dispatch
```

## 11. 정리

다음 명령은 보드와 Profile을 삭제한다. 실습 결과를 확인했고 정리를 원할 때만 실행한다.

```bash
hermes kanban boards switch default
hermes kanban boards show
hermes kanban boards rm service-plan-lab --delete
hermes kanban boards list --all

hermes profile delete infra-planner --yes
hermes profile delete ops-planner --yes
hermes profile delete plan-reviewer --yes
hermes profile list
```

`--delete`를 생략하면 보드는 영구 삭제되지 않고 `_archived`로 이동한다. 실습을 위해 Gateway를 새로 시작한 경우에만 종료한다.

```bash
hermes gateway stop
hermes gateway status
```
