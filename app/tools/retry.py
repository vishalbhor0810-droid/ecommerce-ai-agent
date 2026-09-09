from tenacity import retry, stop_after_attempt, wait_exponential


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(
        multiplier=1,
        min=1,
        max=4
    )
)
def unreliable_operation():
    unreliable_operation.attempts += 1

    print(f"Attempt {unreliable_operation.attempts}")

    if unreliable_operation.attempts < 3:
        raise RuntimeError("Simulated temporary failure")

    return "Operation succeeded"


unreliable_operation.attempts = 0