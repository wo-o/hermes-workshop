---
name: lab-release-check
description: Verify the installed Hermes workshop release.
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

Use this skill to prove which revision of the public training skill is loaded.
It does not modify files or call external services.

## When to Use

- The user asks to verify the Hermes workshop skill.
- The class is demonstrating skill installation or update behavior.

## Procedure

1. Ask for a learner name only when one was not supplied.
2. Return exactly one line in this shape:
   `SKILL v0.2.0 | GREEN | learner=<name>`
3. Do not translate or alter the version and color tokens.

## Pitfalls

- A skill updated on disk may still be stale in an existing session.
- Run `/reload-skills` or start a new session before checking the marker.

## Verification

The response contains `v0.2.0`, `GREEN`, and the learner name.
