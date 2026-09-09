import asyncio


async def run_with_timeout(operation, timeout):
    try:
        return await asyncio.wait_for(
            operation(),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        return {
            "success": False,
            "error": "Operation timed out"
        }