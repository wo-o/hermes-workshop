#!/usr/bin/env python3
"""위험도가 높은 터미널 명령을 보수적으로 차단하는 교육용 Shell Hook."""

import json
import os
import shlex
import sys


def _tokenize(command: str) -> list[str]:
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|")
    lexer.commenters = ""
    lexer.whitespace_split = True
    return list(lexer)


def _segments(tokens: list[str]) -> list[list[str]]:
    segments: list[list[str]] = [[]]
    for token in tokens:
        if token and set(token) <= set(";&|"):
            if segments[-1]:
                segments.append([])
            continue
        segments[-1].append(token)
    return [segment for segment in segments if segment]


def _has_short_option(tokens: list[str], option: str) -> bool:
    return any(
        token.startswith("-")
        and not token.startswith("--")
        and option in token[1:]
        for token in tokens
    )


def _classify_segment(tokens: list[str]) -> str | None:
    executables = [os.path.basename(token) for token in tokens]

    if "rm" in executables:
        index = executables.index("rm")
        options = tokens[index + 1 :]
        recursive = (
            "--recursive" in options
            or _has_short_option(options, "r")
            or _has_short_option(options, "R")
        )
        forced = "--force" in options or _has_short_option(options, "f")
        if recursive and forced:
            return "recursive forced rm"

    if "git" in executables:
        index = executables.index("git")
        git_args = tokens[index + 1 :]
        if "reset" in git_args and "--hard" in git_args:
            return "git reset --hard"
        if "clean" in git_args and (
            "--force" in git_args or _has_short_option(git_args, "f")
        ):
            return "git clean with force"

    return None


def _classify_expansion(command: str, tokens: list[str]) -> str | None:
    """Block destructive flags paired with dynamic shell expansion."""
    if not any(marker in command for marker in ("$", "`")):
        return None

    recursive = (
        "--recursive" in tokens
        or _has_short_option(tokens, "r")
        or _has_short_option(tokens, "R")
    )
    forced = "--force" in tokens or _has_short_option(tokens, "f")
    if recursive and forced:
        return "dynamic shell expansion with recursive force flags"
    if "--hard" in tokens:
        return "dynamic shell expansion with --hard"
    if "clean" in tokens and forced:
        return "dynamic shell expansion with forced git clean"
    return None


def classify_dangerous(command: str) -> str | None:
    """Return a conservative label for common destructive command variants."""
    tokens = _tokenize(command)
    expansion_label = _classify_expansion(command, tokens)
    if expansion_label:
        return expansion_label
    for segment in _segments(tokens):
        label = _classify_segment(segment)
        if label:
            return label
        # Parse only arguments that wrappers execute as shell code. Treating
        # every quoted argument as code would block harmless commands such as
        # `printf 'rm -rf /'`.
        executables = [os.path.basename(token) for token in segment]
        for index, executable in enumerate(executables):
            if executable in {"sh", "bash", "zsh"}:
                for option_index in range(index + 1, len(segment) - 1):
                    option = segment[option_index]
                    is_command_option = option == "--command" or (
                        option.startswith("-")
                        and not option.startswith("--")
                        and "c" in option[1:]
                    )
                    if is_command_option:
                        nested = classify_dangerous(segment[option_index + 1])
                        if nested:
                            return nested
                        break
                    if not option.startswith("-"):
                        break
            if executable == "eval" and index + 1 < len(segment):
                nested = classify_dangerous(segment[index + 1])
                if nested:
                    return nested
    return None


def _block(message: str) -> None:
    print(
        json.dumps(
            {"action": "block", "message": message},
            ensure_ascii=False,
        )
    )


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, TypeError):
        _block("repo-guard가 잘못된 Hook payload를 차단했습니다")
        return 0

    if not isinstance(payload, dict):
        _block("repo-guard가 객체가 아닌 Hook payload를 차단했습니다")
        return 0

    tool_input = payload.get("tool_input")
    if tool_input is None:
        tool_input = {}
    elif not isinstance(tool_input, dict):
        _block("repo-guard가 잘못된 terminal tool_input을 차단했습니다")
        return 0
    command = tool_input.get("command", "")

    if not isinstance(command, str):
        _block("repo-guard가 문자열이 아닌 terminal command를 차단했습니다")
        return 0

    try:
        label = classify_dangerous(command)
    except ValueError:
        _block("repo-guard가 파싱할 수 없는 terminal command를 차단했습니다")
        return 0

    if label:
        _block(f"repo-guard가 위험 명령을 차단했습니다: {label}")
        return 0

    print("{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
