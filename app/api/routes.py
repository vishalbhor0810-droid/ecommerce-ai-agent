from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from app.agent.graph import build_graph
from app.agent.nodes import retriever
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
    result = agent.invoke(
    {
        "query": request.query,
        "session_id": request.session_id
    },
    config={
        "configurable": {
            "thread_id": request.session_id
        }
    }
)

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

    # 5. Return only public fields; the full state holds internals such as
    # the system prompt and raw tool outputs
    return {
        "trace_id": trace_id,
        "query": result.get("query"),
        "masked_query": result.get("masked_query"),
        "injection_detected": result.get("injection_detected", False),
        "intent": result.get("intent"),
        "tools_used": result.get("tools_used", []),
        "answer": result.get("answer")
    }


@router.post("/add_document")
def add_document(request: DocumentRequest):
    # Only accept a plain .md filename, so "../../x" can't write outside KB_DIR
    filename = Path(request.filename).name

    if filename != request.filename or not filename.endswith(".md"):
        raise HTTPException(
            status_code=400,
            detail="Filename must be a plain .md file name, e.g. gift_cards.md"
        )

    # Create directory if it doesn't exist
    KB_DIR.mkdir(parents=True, exist_ok=True)

    file_path = KB_DIR / filename

    # Save document contents
    file_path.write_text(
        request.content,
        encoding="utf-8"
    )

    # Index it in ChromaDB so the agent can retrieve it straight away
    chunks_added = retriever.add_document(filename, request.content)

    return {
        "message": "Document added and indexed successfully",
        "filename": filename,
        "chunks_added": chunks_added
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