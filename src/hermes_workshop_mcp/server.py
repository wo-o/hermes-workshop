"""Minimal stdio MCP server used in the Hermes workshop."""

from mcp.server.fastmcp import FastMCP

VERSION = "0.2.0"
COLOR = "green"

mcp = FastMCP("hermes-workshop")


def get_lab_status(learner: str = "student") -> dict[str, str]:
    """Return deterministic state for tests and demonstrations."""
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
    """Report the installed Hermes workshop MCP version and status."""
    return get_lab_status(learner)


def main() -> None:
    """Run the server over stdio."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
