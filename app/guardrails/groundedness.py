import re

def check_groundedness(answer, context):
    # 1. Ensure answer is a string
    if isinstance(answer, dict):
        answer = answer.get("answer", "")
    elif not isinstance(answer, str):
        answer = str(answer)

    if not answer.strip():
        return False

    # 2. Convert context list/dicts into a single lowercased string
    if isinstance(context, list):
        context_text = " ".join(
            [item.get("text", "") if isinstance(item, dict) else str(item) for item in context]
        ).lower()
    elif isinstance(context, str):
        context_text = context.lower()
    else:
        context_text = str(context).lower()

    # 3. Extract words from answer
    answer_words = re.findall(r'\b\w+\b', answer.lower())
    if not answer_words:
        return False

    # 4. Check word matches against context_text
    matches = sum(1 for word in answer_words if word in context_text)
    
    # Simple overlap ratio check (returns True if at least 50% of answer words exist in context)
    overlap = matches / len(answer_words)
    return overlap >= 0.5