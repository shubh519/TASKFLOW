import re


# Priority keywords — checked in this exact order
HIGH_PRIORITY_KEYWORDS = ["urgent", "asap", "high priority"]
LOW_PRIORITY_KEYWORDS = ["whenever", "low priority"]


# Due-date phrases — checked in this exact order
DUE_DATE_PHRASES = [
    "today",
    "tomorrow",
    "next week",
    "next monday",
    "next tuesday",
    "next wednesday",
    "next thursday",
    "next friday",
    "next saturday",
    "next sunday",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]


def _remove_phrase(text: str, phrase: str) -> str:
    """Remove every occurrence of a matched phrase, case-insensitively."""
    pattern = re.compile(re.escape(phrase), re.IGNORECASE)
    return pattern.sub("", text)


def parse_task_description(description: str) -> dict:
    """
    Deterministic mock parser used by the AI quick-add endpoint.

    Returns:
        {
            "title": str,
            "priority": "low" | "medium" | "high",
            "due_date_hint": str | None
        }
    """

    original_text = description
    lower_text = description.lower()

    # -------------------------
    # 1. Determine priority
    # -------------------------
    priority = "medium"
    matched_priority_phrase = None

    for keyword in HIGH_PRIORITY_KEYWORDS:
        if keyword in lower_text:
            priority = "high"
            matched_priority_phrase = keyword
            break

    if matched_priority_phrase is None:
        for keyword in LOW_PRIORITY_KEYWORDS:
            if keyword in lower_text:
                priority = "low"
                matched_priority_phrase = keyword
                break

    # -------------------------
    # 2. Determine due date
    # -------------------------
    due_date_hint = None

    for phrase in DUE_DATE_PHRASES:
        if phrase in lower_text:
            due_date_hint = phrase
            break

    # -------------------------
    # 3. Build title
    # -------------------------
    title = original_text

    if matched_priority_phrase:
        title = _remove_phrase(title, matched_priority_phrase)

    if due_date_hint:
        title = _remove_phrase(title, due_date_hint)

    title = title.strip()

    if not title:
        title = "Untitled task"

    return {
        "title": title,
        "priority": priority,
        "due_date_hint": due_date_hint,
    }