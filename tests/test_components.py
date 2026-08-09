import importlib.util
import json
import re
import subprocess
from pathlib import Path

from hermes_workshop_mcp.server import get_lab_status

ROOT = Path(__file__).parents[1]

WORKSHOP_SKILLS = {
    "meeting-action-items",
    "systematic-bug-fix",
    "tdd-feature-workflow",
    "github-issue-spec",
    "verified-readme",
}


def _load_plugin_tools():
    spec = importlib.util.spec_from_file_location(
        "demo_plugin_tools", ROOT / "plugin_tools.py"
    )
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _load_plugin_hooks():
    spec = importlib.util.spec_from_file_location(
        "demo_plugin_hooks", ROOT / "plugin_hooks.py"
    )
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_plugin_greeting_reports_v03():
    result = json.loads(_load_plugin_tools().course_greeting({"name": "Hermes"}))
    assert result == {
        "component": "plugin",
        "version": "0.3.0",
        "color": "green",
        "message": "안녕하세요, Hermes님! Hermes 워크숍이 준비되었습니다.",
    }


def test_plugin_rejects_blank_name():
    result = json.loads(_load_plugin_tools().course_greeting({"name": "  "}))
    assert result == {"error": "name이 필요합니다"}


def test_plugin_prefixes_final_response_once():
    hook = _load_plugin_hooks().prefix_hello_world
    assert hook("OK") == "Hello World!\nOK"
    assert hook("Hello World!\nOK") == "Hello World!\nOK"


def test_gateway_restart_hook_files_are_present():
    hook_dir = ROOT / "hooks" / "hello-world-restart"
    manifest = (hook_dir / "HOOK.yaml").read_text()
    handler = (hook_dir / "handler.py").read_text()
    assert "gateway:startup" in manifest
    assert 'logger.info("Hello World!")' in handler


def test_shell_hook_examples_are_present():
    hook_dir = ROOT / "agent-hooks"
    assert (hook_dir / "repo-guard.py").is_file()
    assert (hook_dir / "inject-git-status.py").is_file()


def _run_shell_hook(name: str, payload: dict) -> dict:
    result = subprocess.run(
        [str(ROOT / "agent-hooks" / name)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def test_repo_guard_blocks_destructive_git_command():
    result = _run_shell_hook(
        "repo-guard.py",
        {"tool_input": {"command": "git reset --hard"}},
    )
    assert result["action"] == "block"
    assert "git reset --hard" in result["message"]


def test_repo_guard_allows_safe_command():
    assert _run_shell_hook(
        "repo-guard.py",
        {"tool_input": {"command": "git status --short"}},
    ) == {}


def test_git_status_hook_returns_context():
    result = _run_shell_hook("inject-git-status.py", {"cwd": str(ROOT)})
    assert result["context"].startswith("현재 작업 디렉터리의 git status:\n")


def test_mcp_status_reports_v02():
    assert get_lab_status(" Techwoo ") == {
        "component": "mcp",
        "version": "0.2.0",
        "color": "green",
        "learner": "Techwoo",
        "status": "ready",
    }


def test_skill_marker_reports_v02():
    content = (ROOT / "skills" / "lab-release-check" / "SKILL.md").read_text()
    assert "version: 0.2.0" in content
    assert "SKILL v0.2.0 | GREEN" in content


def test_workshop_skills_have_valid_frontmatter_and_sections():
    for name in WORKSHOP_SKILLS:
        content = (ROOT / "skills" / name / "SKILL.md").read_text()
        assert content.startswith("---\n")
        frontmatter, body = content[4:].split("\n---\n", 1)
        assert f"name: {name}" in frontmatter
        description = re.search(r"^description: (.+)$", frontmatter, re.MULTILINE)
        assert description is not None
        assert len(description.group(1)) <= 60
        assert description.group(1).endswith(".")
        assert "author: Techwoo (wo-o), Hermes Agent" in frontmatter
        assert "platforms: [linux, macos, windows]" in frontmatter
        assert "## 사용 시점" in body
        assert "## 주의 사항" in body
        assert "## 검증" in body


def test_skill_workshop_inputs_are_present():
    inputs = ROOT / "examples" / "skill-inputs"
    lab = ROOT / "examples" / "skill-lab"
    assert (ROOT / "SKILLS.md").is_file()
    assert (inputs / "meeting-notes.md").is_file()
    assert (inputs / "email-validator-spec.md").is_file()
    assert (inputs / "issue-request.md").is_file()
    assert (inputs / "README.bad.md").is_file()
    assert (lab / "discount.py").is_file()
    assert (lab / "test_discount.py").is_file()
    assert (lab / "email_validator.py").is_file()
