from typing import List, Optional
from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    answer: str
    source: str
    tools_used: List[str] = Field(default_factory=list)
    similarity: Optional[float] = None
    order_id: Optional[str] = None
    amount: Optional[float] = None
    escalation_score: Optional[float] = None
    escalation_required: bool = False
    grounded: bool = False