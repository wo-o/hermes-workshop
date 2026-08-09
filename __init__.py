"""네이티브 Hermes 플러그인 등록 진입점."""

from . import schemas, tools


def register(ctx):
    """Hermes가 이 플러그인을 로드할 때 데모 도구를 등록한다."""
    ctx.register_tool(
        name="course_greeting",
        toolset="workshop-greeting",
        schema=schemas.COURSE_GREETING,
        handler=tools.course_greeting,
    )
