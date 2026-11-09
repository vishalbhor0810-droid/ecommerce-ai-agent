import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from tenacity import retry, stop_after_attempt, wait_exponential


PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Covers starting the MCP server process and the tool call itself
MCP_TIMEOUT_SECONDS = 20


async def _call_check_order(order_id):
    """
    Start the ShopEase MCP server over stdio and call its check_order tool.
    """

    server = StdioServerParameters(
        command=sys.executable,
        args=["-m", "app.tools.mcp_server"],
        cwd=str(PROJECT_ROOT)
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "check_order",
                {"order_id": order_id}
            )

    if result.isError:
        raise RuntimeError(f"MCP tool error: {result.content}")

    # Newer MCP versions return structured output; older ones return JSON text
    if result.structuredContent:
        data = result.structuredContent
        if set(data.keys()) == {"result"}:
            data = data["result"]
    else:
        data = json.loads(result.content[0].text)

    if "error" in data:
        raise RuntimeError(data["error"])

    return data


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(
        multiplier=1,
        min=1,
        max=4
    ),
    reraise=True
)
def _check_order_with_retry(order_id):
    return asyncio.run(
        asyncio.wait_for(
            _call_check_order(order_id),
            timeout=MCP_TIMEOUT_SECONDS
        )
    )


def check_order_via_mcp(order_id):
    """
    Look up an order through the MCP server, with timeout and retries.
    Returns an error result instead of raising if the service stays down.
    """

    try:
        return _check_order_with_retry(order_id)
    except Exception as e:
        return {
            "found": False,
            "order_id": order_id,
            "message": (
                "The order service is temporarily unavailable. "
                "Please try again in a few minutes."
            ),
            "error": str(e)
        }
