import re


# =========================================================
# PRIORITY KEYWORDS
# =========================================================

# Checked first
HIGH_PRIORITY_KEYWORDS = [
    "urgent",
    "asap",
]

# Checked only if no high-priority keyword matched
LOW_PRIORITY_KEYWORDS = [
    "whenever",
    "low priority",
]


# =========================================================
# DUE-DATE PHRASES
# =========================================================

# Checked in this exact order
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


# =========================================================
# ROLE-BASED PROMPT STRUCTURE
# =========================================================

SYSTEM_PROMPT = """
You are a TaskFlow task parser.

Convert a free-text task description into structured task data.

Return these fields:
- title
- priority
- due_date_hint

Priority must be exactly one of:
low, medium, high.

Use the deterministic TaskFlow parsing rules.
"""


def build_prompt_messages(description: str) -> list[dict]:
    """
    Build standard role-based messages.

    The deterministic mock parser remains the
    default implementation.

    No API key is required.
    No network request is made.
    """

    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT.strip(),
        },
        {
            "role": "user",
            "content": description,
        },
    ]


# =========================================================
# HELPER
# =========================================================

def _remove_phrase(text: str, phrase: str) -> str:
    """
    Remove every occurrence of a phrase
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

    # -----------------------------------------------------
    # STEP 0: Build role-based prompt messages
    # -----------------------------------------------------

    messages = build_prompt_messages(description)

    # The deterministic mock reads the same user-role
    # content that would be supplied to a real LLM.
    original_text = messages[1]["content"]

    # Lower-case working copy is used only
    # for deterministic keyword matching.
    lower_text = original_text.lower()

    # -----------------------------------------------------
    # STEP 1: Determine priority
    # -----------------------------------------------------

    priority = "medium"
    matched_priority_keywords = []

    # Group 1: high priority
    # This group is checked first.
    if any(
        keyword in lower_text
        for keyword in HIGH_PRIORITY_KEYWORDS
    ):
        priority = "high"
        matched_priority_keywords = (
            HIGH_PRIORITY_KEYWORDS
        )

    # Group 2: low priority
    # Checked only when the high-priority
    # group did not match.
    elif any(
        keyword in lower_text
        for keyword in LOW_PRIORITY_KEYWORDS
    ):
        priority = "low"
        matched_priority_keywords = (
            LOW_PRIORITY_KEYWORDS
        )

    # If neither group matches,
    # priority remains "medium".

    # -----------------------------------------------------
    # STEP 2: Determine due-date hint
    # -----------------------------------------------------

    due_date_hint = None

    for phrase in DUE_DATE_PHRASES:
        if phrase in lower_text:
            due_date_hint = phrase
            break

    # -----------------------------------------------------
    # STEP 3: Build title
    # -----------------------------------------------------

    # Start from the original-cased description.
    title = original_text

    # Remove every occurrence of every keyword
    # from the priority group that matched.
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

    # Only remove leading/trailing whitespace.
    title = title.strip()

    # Exact fallback required by the assignment.
    if not title:
        title = "Untitled task"

    # -----------------------------------------------------
    # FINAL STRUCTURED RESULT
    # -----------------------------------------------------

    return {
        "title": title,
        "priority": priority,
        "due_date_hint": due_date_hint,
    }