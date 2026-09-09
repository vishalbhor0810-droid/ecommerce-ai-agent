from typing import TypedDict, List, Dict, Optional


class AgentState(TypedDict, total=False):

    query: str

    masked_query: str

    injection_detected: bool

    intent: str

    retrieved_context: List[Dict]

    order_result: Dict

    answer: str

    source: Optional[str]

    similarity: float

    escalation_required: bool

    conversation_history: List[Dict]