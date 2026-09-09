import re
import os
from groq import Groq

from app.rag.retriever import RAGRetriever
from app.rag.pipeline import RAG_THRESHOLD
from app.tools.order_tool import get_order_status
from app.memory.memory import ConversationMemory
from app.models.schemas import AgentResponse
from app.guardrails.pii import mask_pii
from app.guardrails.injection import detect_prompt_injection

from app.guardrails.groundedness import check_groundedness


retriever = RAGRetriever()


def pii_guardrail(state):
    query = state["query"]
    masked_query = mask_pii(query)

    return {
        "query": masked_query,
        "masked_query": masked_query
    }

def injection_guardrail(state):
    query = state["query"]

    detected = detect_prompt_injection(query)

    return {
        "injection_detected": detected
    }

def injection_block_node(state):
    return {
        "answer": (
            "I’m sorry, but I can’t follow requests to "
            "override or reveal my internal instructions."
        ),
        "source": "guardrail"
    }

def classify_query(state):

    query = state["query"]
    query_lower = query.lower()
    history = state.get("conversation_history", [])

    # 1. Direct Order ID match in current query
    if re.search(r"\bord\d+\b", query_lower):
        return {"intent": "order"}

    # 2. Follow-up order inquiry check using history
    order_followup_keywords = ["order", "that order", "amount", "status", "cost", "it"]
    if any(kw in query_lower for kw in order_followup_keywords):
        for msg in reversed(history):
            content = msg.get("content", "").lower()
            match = re.search(r"\b(ord\d+)\b", content)
            if match:
                extracted_id = match.group(1).upper()
                return {
                    "intent": "order",
                    "query": f"{query} ({extracted_id})"
                }

    # 3. RAG Keyword Checks
    rag_keywords = [
        "return", "refund", "shipping", "cancel", "track", 
        "payment", "cash", "exchange", "warranty", "damaged", 
        "delivery", "privacy", "support"
    ]

    if any(keyword in query_lower for keyword in rag_keywords):
        return {"intent": "rag"}

    # 4. If conversation history exists and it's a general follow-up, route to RAG
    if history:
        return {"intent": "rag"}

    return {"intent": "unknown"}


def retrieve_kb(state):

    query = state["query"]

    results = retriever.search(
        query,
        strategy="sentence",
        top_k=3
    )

    if not results:

        return {
            "retrieved_context": [],
            "similarity": 0.0
        }

    return {
        "retrieved_context": results,
        "similarity": results[0]["similarity"]
    }


def order_tool_node(state):

    query = state["query"]

    match = re.search(
        r"\b(ORD\d+)\b",
        query.upper()
    )

    if not match:

        return {
            "order_result": {
                "found": False,
                "message": "No order ID found."
            }
        }

    order_id = match.group(1)

    result = get_order_status(order_id)

    return {
        "order_result": result
    }


def fallback_node(state):

    return {
        "answer": (
            "I'm sorry, but I can only help with "
            "ShopEase e-commerce support questions."
        )
    }


def generate_answer(state):

    intent = state.get("intent")

    if intent == "order":

        order_result = state.get("order_result", {})

        if not order_result.get("found"):
            answer = "I could not find that order. Please check the order ID and try again."
            escalation_required = False
        else:
            escalation = order_result.get("escalation_score", 0.0)
            escalation_required = escalation >= 0.6
            answer = (
                f"Order {order_result['order_id']} is currently {order_result['status']}. "
                f"The order amount is ₹{order_result['amount']:.2f}. "
                f"Escalation score: {escalation:.2f}."
            )

        validated = AgentResponse(
            answer=answer,
            source="order_tool",
            order_id=order_result.get("order_id"),
            amount=order_result.get("amount"),
            escalation_score=order_result.get("escalation_score"),
            escalation_required=escalation_required
        )

        return {
            "answer": validated.model_dump_json()
        }

    if intent == "rag":

        results = state.get("retrieved_context", [])

        if not results:
            answer = "I don't have enough information in the knowledge base to answer that."
            validated = AgentResponse(
                answer=answer,
                source="knowledge_base",
                similarity=state.get("similarity")
            )
            return {
                "answer": validated.model_dump_json()
            }

        best_similarity = results[0]["similarity"]

        if best_similarity < RAG_THRESHOLD:
            answer = "I don't have enough information in the knowledge base to answer that."
            validated = AgentResponse(
                answer=answer,
                source="knowledge_base",
                similarity=state.get("similarity")
            )
            return {
                "answer": validated.model_dump_json()
            }

        context = "\n\n".join(
            f"Source: {result['source']}\n"
            f"{result['text']}"
            for result in results
        )

        history = state.get("conversation_history", [])

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a ShopEase customer support assistant. "
                    "Answer only using the provided knowledge base context "
                    "and relevant conversation history. "
                    "Do not invent information."
                )
            }
        ]

        for message in history:
            messages.append({
                "role": message["role"],
                "content": message["content"]
            })

        messages.append({
            "role": "user",
            "content": f"""Knowledge Base Context:
{context}

Current Question:
{state['query']}"""
        })

        client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages
        )

        answer = response.choices[0].message.content

        grounded = check_groundedness(
                answer,
                state.get("retrieved_context", [])
            )

        if not grounded:
            answer = (
                "I'm sorry, but I could not verify that answer "
                "from my knowledge base."
            )

        validated = AgentResponse(
            answer=answer,
            source="knowledge_base",
            similarity=state.get("similarity"),
            grounded=grounded
        )

        return {
            "answer": validated.model_dump_json()
        }

    # Fallback branch
    answer = state.get(
        "answer",
        "I'm sorry, but I can only help with ShopEase e-commerce support questions."
    )

    validated = AgentResponse(
        answer=answer,
        source="fallback"
    )

    return {
        "answer": validated.model_dump_json()
    }


def save_memory(state):

    memory = ConversationMemory("demo_session")

    query = state.get("query")
    answer = state.get("answer")

    if query:
        memory.add_message("user", query)
    if answer:
        memory.add_message("assistant", answer)

    return {}