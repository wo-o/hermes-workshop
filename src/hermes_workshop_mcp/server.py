"""Hermes 워크숍에서 사용하는 최소 구성의 stdio MCP 서버."""

from mcp.server.fastmcp import FastMCP

VERSION = "0.2.0"
COLOR = "green"

mcp = FastMCP("hermes-workshop")


def get_lab_status(learner: str = "student") -> dict[str, str]:
    """테스트와 시연을 위해 항상 동일한 상태를 반환한다."""
    cleaned = learner.strip() or "student"
    return {
        "component": "mcp",
        "version": VERSION,
        "color": COLOR,
        "learner": cleaned,
        "status": "ready",
    }


@mcp.tool()
def lab_status(learner: str = "student") -> dict[str, str]:
    """설치된 Hermes 워크숍 MCP의 버전과 상태를 보고합니다."""
    return get_lab_status(learner)


def main() -> None:
    """stdio로 서버를 실행한다."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
