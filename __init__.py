"""Native Hermes plugin registration entry point."""

from . import schemas, tools


def register(ctx):
    """Register the demo tool when Hermes loads this plugin."""
    ctx.register_tool(
        name="course_greeting",
        toolset="workshop-greeting",
        schema=schemas.COURSE_GREETING,
        handler=tools.course_greeting,
    )
