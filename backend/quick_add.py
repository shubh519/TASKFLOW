import re


# Priority keyword groups — checked in this exact order
HIGH_PRIORITY_KEYWORDS = [
    "urgent",
    "asap",
    "high priority",
]

LOW_PRIORITY_KEYWORDS = [
    "whenever",
    "low priority",
]


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
    """
    Remove every occurrence of a phrase,
    case-insensitively.
    """
    pattern = re.compile(
        re.escape(phrase),
        re.IGNORECASE,
    )

    return pattern.sub("", text)
# =========================================================
# DETERMINISTIC QUICK-ADD PARSER
# =========================================================

# Deterministic Quick-Add parser used by the TaskFlow API.
def parse_task_description(description: str) -> dict:
    """
    Deterministic mock parser for TaskFlow Quick Add.

    No API key.
    No network calls.

    Returns:
    {
        "title": str,
        "priority": "low" | "medium" | "high",
        "due_date_hint": str | None
    }
    """

    original_text = description
    lower_text = description.lower()

    # --------------------------------
    # STEP 1: Determine priority
    # --------------------------------

    priority = "medium"
    matched_priority_keywords = []

    # Group 1 — high priority
    if any(
        keyword in lower_text
        for keyword in HIGH_PRIORITY_KEYWORDS
    ):
        priority = "high"
        matched_priority_keywords = HIGH_PRIORITY_KEYWORDS

    # Group 2 — low priority
    elif any(
        keyword in lower_text
        for keyword in LOW_PRIORITY_KEYWORDS
    ):
        priority = "low"
        matched_priority_keywords = LOW_PRIORITY_KEYWORDS

    # --------------------------------
    # STEP 2: Determine due date
    # --------------------------------

    due_date_hint = None

    for phrase in DUE_DATE_PHRASES:
        if phrase in lower_text:
            due_date_hint = phrase
            break

    # --------------------------------
    # STEP 3: Create title
    # --------------------------------

    title = original_text

    # Remove every occurrence of every keyword
    # from ONLY the priority group that matched.
    for keyword in matched_priority_keywords:
        title = _remove_phrase(
            title,
            keyword,
        )

    # Remove every occurrence of the matched
    # due-date phrase.
    if due_date_hint:
        title = _remove_phrase(
            title,
            due_date_hint,
        )

    # Trim only leading/trailing whitespace.
    title = title.strip()

    # Title must never be empty.
    if not title:
        title = "Untitled task"

    return {
        "title": title,
        "priority": priority,
        "due_date_hint": due_date_hint,
    }