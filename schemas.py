"""Tool schemas exposed by the demo Hermes plugin."""

COURSE_GREETING = {
    "name": "course_greeting",
    "description": (
        "Return a deterministic FastCampus course greeting with the installed "
        "plugin version. Use it when verifying this demo plugin installation."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Name of the person to greet.",
            }
        },
        "required": ["name"],
    },
}
