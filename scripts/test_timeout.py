import asyncio


async def slow_node():
    await asyncio.sleep(3)
    return "Completed"


async def main():
    try:
        result = await asyncio.wait_for(
            slow_node(),
            timeout=2
        )
        print(result)

    except asyncio.TimeoutError:
        print({
            "success": False,
            "error": "Global agent timeout"
        })


if __name__ == "__main__":
    asyncio.run(main())
# import asyncio

# from app.agent.timeouts import run_with_timeout


# async def slow_node():
#     await asyncio.sleep(3)
#     return "Completed"


# async def main():
#     try:
#         result = await asyncio.wait_for(
#             slow_node(),
#             timeout=2
#         )

#         print(result)

#     except asyncio.TimeoutError:
#         print({
#             "success": False,
#             "error": "Global agent timeout"
#         })
        
# async def main():
#     result = await run_with_timeout(
#         slow_node,
#         timeout=1
#     )

#     print(result)


# if __name__ == "__main__":
#     asyncio.run(main())