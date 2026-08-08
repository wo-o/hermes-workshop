"""Tool handlers for the demo Hermes plugin."""

import json

VERSION = "0.2.0"
COLOR = "green"


def course_greeting(args, **kwargs) -> str:
    """Return a stable JSON response and never leak an exception."""
    del kwargs
    try:
        name = str(args.get("name", "")).strip()
        if not name:
            return json.dumps({"error": "name is required"})
        return json.dumps(
            {
                "component": "plugin",
                "version": VERSION,
                "color": COLOR,
                "message": f"Hello, {name}! Hermes workshop is ready.",
            }
        )
    except Exception as exc:
        return json.dumps({"error": f"course greeting failed: {exc}"})
