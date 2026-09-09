import logging
import uuid
import time
from app.guardrails.pii import mask_pii

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

def create_trace_id():
    return str(uuid.uuid4())

def log_request(trace_id, query, start_time, answer):
    elapsed = round(time.time() - start_time, 4)

    # Convert query and answer to strings to prevent string-method crashes in mask_pii
    safe_query = str(query) if query else ""
    safe_answer = str(answer) if answer else ""

    logging.info(
        "trace_id=%s | query=%s | answer=%s | elapsed=%ss",
        trace_id,
        mask_pii(safe_query),
        mask_pii(safe_answer),
        elapsed
    )