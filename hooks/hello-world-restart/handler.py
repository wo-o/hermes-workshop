"""게이트웨이가 시작될 때 Hello World!를 기록한다."""

import logging

logger = logging.getLogger("hooks.hello-world-restart")


async def handle(event_type: str, context: dict) -> None:
    """Handle the gateway startup event."""
    logger.info("Hello World!")
