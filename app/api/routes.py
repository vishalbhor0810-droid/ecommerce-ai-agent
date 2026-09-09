from pathlib import Path
from fastapi import APIRouter
from pydantic import BaseModel
import json
from app.agent.graph import build_graph
import time

from app.logging.logger import create_trace_id, log_request

router = APIRouter()

# Initialize the agent graph
agent = build_graph()

# Base directory for Knowledge Base files
KB_DIR = Path("data/knowledge_base")


class AskRequest(BaseModel):
    query: str
    session_id: str = "default"


class DocumentRequest(BaseModel):
    filename: str
    content: str


@router.post("/ask")
def ask(request: AskRequest):
    trace_id = create_trace_id()
    start_time = time.time()

    # 1. Invoke the graph
    result = agent.invoke({
        "query": request.query
    })

    # 2. Safely extract answer as string for logger
    raw_answer = result.get("answer", "")
    answer_str = str(raw_answer) if raw_answer is not None else ""

    # 3. Log the request safely
    log_request(
        trace_id,
        request.query,
        start_time,
        answer_str
    )

    # 4. Parse inner JSON string for response output if applicable
    try:
        if isinstance(raw_answer, str):
            result["answer"] = json.loads(raw_answer)
    except Exception:
        pass

    return {
        "trace_id": trace_id,
        **result
    }


@router.post("/add_document")
def add_document(request: DocumentRequest):
    # Create directory if it doesn't exist
    KB_DIR.mkdir(parents=True, exist_ok=True)

    file_path = KB_DIR / request.filename

    # Save document contents
    file_path.write_text(
        request.content,
        encoding="utf-8"
    )

    return {
        "message": "Document added successfully",
        "filename": request.filename
    }
# from fastapi import APIRouter
# from pydantic import BaseModel

# from app.agent.graph import app


# router = APIRouter()


# class AskRequest(BaseModel):
#     query: str
#     session_id: str = "default"


# @router.post("/ask")
# def ask(request: AskRequest):
#     result = app.invoke({
#         "query": request.query
#     })

#     return result