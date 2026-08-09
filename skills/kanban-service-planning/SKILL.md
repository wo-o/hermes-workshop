---
name: kanban-service-planning
description: Hermes Kanban 다중 Profile 협업 실습을 진행합니다.
version: 0.1.0
author: Techwoo (wo-o), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Hermes, Kanban, Profiles, Workshop]
    related_skills: []
---

# Kanban Service Planning

여러 Hermes Profile이 인프라 계획과 운영 계획을 병렬로 작성하고, 의존 작업이 두 결과를 최종 출시 체크리스트로 통합하게 한다. 실제 인프라는 생성하지 않는다.

## 사용 시점

- Hermes Kanban의 작업 배정, 병렬 실행, parent 의존성을 실습할 때
- 여러 Profile의 역할 분담과 결과 통합을 검증할 때
- `block`, `comment`, `unblock`, `reclaim` 복구 흐름을 연습할 때

다른 서비스의 실제 배포나 클라우드 프로비저닝에는 사용하지 않는다.

## 사전 조건

1. `terminal`로 `hermes --version`을 실행하여 Hermes Agent v0.20.0 이상인지 확인한다.
2. `terminal`로 `hermes kanban --help`, `hermes profile create --help`를 확인한다.
3. 기존 `infra-planner`, `ops-planner`, `plan-reviewer` Profile과 `service-plan-lab` 보드가 있는지 확인한다. 기존 자산은 자동으로 덮어쓰거나 삭제하지 않는다.

## 실행 방법

전체 실습은 `references/lab.md`를 먼저 읽고 순서대로 진행한다. 명령을 대신 실행하는 경우 각 `hermes kanban create`의 실제 출력에서 task ID를 기록한 뒤 후속 `--parent`와 조회 명령에 사용한다.

## 절차

1. 세 역할의 Profile을 `default`에서 복제하고 `hermes kanban assignees`에서 확인한다.
2. `service-plan-lab` 보드를 만들고 해당 보드로 전환한다.
3. Gateway 상태를 확인한 뒤, 필요한 경우에만 시작한다.
4. 인프라 계획과 운영 계획 카드를 만들고 실제 task ID를 기록한다.
5. 두 ID를 parent로 갖는 최종 계획 카드를 만든다.
6. dry-run 후 최대 두 작업을 병렬 dispatch한다.
7. parent 두 건이 `done`이 된 뒤 최종 카드가 `todo → ready → running → done`으로 이동했는지 확인한다.
8. 최종 작업의 `show`, `runs`, `log`를 확인한다.
9. 정리는 사용자가 명시적으로 요청한 경우에만 수행한다.

## 주의 사항

- 작업 ID를 예시 값으로 추측하지 않는다.
- Gateway가 기존 용도로 실행 중이면 실습 종료 시 중지하지 않는다.
- `hermes kanban boards rm ... --delete`와 `hermes profile delete`는 영구 삭제이므로 자동 실행하지 않는다.
- Profile 이름이나 보드가 이미 존재하면 재사용 여부를 사용자에게 확인하고, 저위험 기본값으로는 별도 이름을 사용한다.
- 명령 접수와 worker의 최종 완료를 같은 성공으로 보고하지 않는다.

## 검증

- 두 parent 카드가 각각 인프라 구성요소와 운영·복구 계획을 포함한다.
- 최종 카드가 두 parent 결과를 모두 받아 우선순위, 담당자, 선행 조건, 미결정 사항, 출시 가능 기준을 포함한다.
- 실제 클라우드나 서버를 만들었다고 표현하지 않는다.
- `hermes kanban stats`와 각 카드의 `runs`에 성공한 실행 기록이 남는다.
