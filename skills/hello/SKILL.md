---
name: hello
description: 이름을 받아 정해진 형식의 인사말을 출력합니다.
version: 0.1.0
author: Techwoo (wo-o), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [workshop, greeting, hello]
    related_skills: []
---

# Hello 인사말

사용자 이름을 받아 일관된 한 줄 인사말을 반환하는 가장 단순한 교육용 스킬입니다. 파일 수정이나 외부 도구 호출은 하지 않습니다.

## 사용 시점

- 사용자가 `/hello` 호출 또는 인사를 요청할 때
- 정해진 출력 형식의 간단한 스킬을 시연할 때

## 절차

1. 이름이 제공되지 않았으면 사용자에게 이름을 물어봅니다.
2. 이름을 받으면 정확히 `안녕하세요, {이름}님!` 형식으로 출력합니다.

## 주의 사항

- 이름을 추측하거나 임의의 호칭으로 바꾸지 않습니다.
- 인사 외의 설명을 덧붙이지 않습니다.

## 검증

응답에 제공된 이름과 `안녕하세요,` 및 `님!` 인사말이 모두 포함되어야 합니다.
