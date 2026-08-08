import importlib.util
import json
from pathlib import Path

from fastcampus_hermes_lab.server import get_lab_status


ROOT = Path(__file__).parents[1]


def _load_plugin_tools():
    spec = importlib.util.spec_from_file_location("demo_plugin_tools", ROOT / "tools.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_plugin_greeting_reports_v02():
    result = json.loads(_load_plugin_tools().course_greeting({"name": "Hermes"}))
    assert result == {
        "component": "plugin",
        "version": "0.2.0",
        "color": "green",
        "message": "Hello, Hermes! FastCampus extension lab is ready.",
    }


def test_plugin_rejects_blank_name():
    result = json.loads(_load_plugin_tools().course_greeting({"name": "  "}))
    assert result == {"error": "name is required"}


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
