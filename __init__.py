"""네이티브 Hermes 플러그인 등록 진입점."""

from .plugin_hooks import prefix_hello_world
from .plugin_tools import course_greeting
from .schemas import COURSE_GREETING


def register(ctx):
    """Hermes가 이 플러그인을 로드할 때 데모 도구와 훅을 등록한다."""
    ctx.register_tool(
        name="course_greeting",
        toolset="workshop-greeting",
        schema=COURSE_GREETING,
        handler=course_greeting,
    )
    ctx.register_hook("transform_llm_output", prefix_hello_world)
