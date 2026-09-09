import re


INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?prior\s+instructions",
    r"forget\s+(all\s+)?previous\s+instructions",
    r"reveal\s+(your\s+)?system\s+prompt",
    r"show\s+(me\s+)?your\s+system\s+prompt",
    r"disclose\s+(your\s+)?instructions",
    r"bypass\s+(your\s+)?rules",
]


def detect_prompt_injection(text: str) -> bool:
    text = text.lower()

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text):
            return True

    return False