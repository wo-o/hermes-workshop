---
name: lab-release-check
description: 설치된 Hermes 워크숍 릴리스를 확인합니다.
version: 0.2.0
author: Techwoo (wo-o), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, workshop, release-check]
    related_skills: []
---

# Lab Release Check

이 공개 교육용 스킬의 어떤 리비전이 로드되어 있는지 증명할 때 사용합니다.
파일을 수정하거나 외부 서비스를 호출하지 않습니다.

## 사용 시점

- 사용자가 Hermes 워크숍 스킬 확인을 요청할 때
- 수업에서 스킬 설치 또는 업데이트 동작을 시연할 때

## 절차

1. 수강생 이름이 주어지지 않은 경우에만 이름을 물어봅니다.
2. 정확히 아래 형식의 한 줄을 반환합니다:
   `SKILL v0.2.0 | GREEN | learner=<name>`
3. 버전과 색상 토큰은 번역하거나 바꾸지 않습니다.

## 주의 사항

- 디스크에서 스킬이 업데이트돼도 기존 세션에는 이전 버전이 남아 있을 수 있습니다.
- 마커를 확인하기 전에 `/reload-skills`를 실행하거나 새 세션을 시작하세요.

## 검증

응답에 `v0.2.0`, `GREEN`, 수강생 이름이 포함되어 있어야 합니다.
