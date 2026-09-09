import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server = StdioServerParameters(
        command="python",
        args=["-m", "app.tools.mcp_server"]
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Test ORD1001
            print("=" * 40)
            print("Testing ORD1001 via MCP:")
            result1 = await session.call_tool(
                "check_order",
                {"order_id": "ORD1001"}
            )
            print(result1)

            # Test ORD1002
            print("=" * 40)
            print("Testing ORD1002 via MCP:")
            result2 = await session.call_tool(
                "check_order",
                {"order_id": "ORD1002"}
            )
            print(result2)


if __name__ == "__main__":
    asyncio.run(main())