from typing import TypedDict, List, Dict, Optional


class AgentState(TypedDict, total=False):

    query: str

    session_id: str

    masked_query: str

    injection_detected: bool

    # Derived from the tools the LLM chose: "rag", "order", "rag+order" or "general"
    intent: str

    # Running LLM conversation for this turn, including tool calls and results
    messages: List[Dict]

    tools_used: List[str]

    tool_iterations: int

    llm_error: bool

    retrieved_context: List[Dict]

    order_results: List[Dict]

    answer: str

    source: Optional[str]

    similarity: Optional[float]

    conversation_history: List[Dict]
