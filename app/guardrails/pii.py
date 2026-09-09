import re


EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
PHONE_PATTERN = r'\b(?:\+91[-\s]?)?[6-9]\d{9}\b'


def mask_pii(text: str) -> str:
    text = re.sub(EMAIL_PATTERN, "***EMAIL***", text)
    text = re.sub(PHONE_PATTERN, "***PHONE***", text)

    return text


def contains_pii(text: str) -> bool:
    return bool(
        re.search(EMAIL_PATTERN, text)
        or re.search(PHONE_PATTERN, text)
    )