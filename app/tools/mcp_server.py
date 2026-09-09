import sys
from mcp.server.fastmcp import FastMCP
from app.tools.order_tool import get_order_status

# Initialize FastMCP Server
mcp = FastMCP("ShopEase Order Service")

@mcp.tool()
def check_order(order_id: str) -> dict:
    """Get order status, amount and escalation score."""
    try:
        return get_order_status(order_id)
    except Exception as e:
        return {"error": f"Failed to retrieve order status: {str(e)}"}

if __name__ == "__main__":
    # Standard mcp.run() defaults to stdio, which is required for the client test script
    mcp.run()