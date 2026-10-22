"""Pure text parsing utilities - no external dependencies."""


def extract_questions_after_think(text: str) -> str:
    """Extract content after the first ' response' delimiter in an LLM output.

    The Together Qwen model separates its reasoning from the final answer
    with a ` response` marker. This function strips everything before
    (and including) the first occurrence of ` response` and returns only
    the answer portion.

    Args:
        text: Raw response text from the LLM.

    Returns:
        The text content after (and excluding) the first ` response`
        delimiter, stripped of leading/trailing whitespace. If ` response`
        is not found, returns the original text stripped.

    Examples:
        >>> extract_questions_after_think(" response1. Question one?\n2. Question two?")
        '1. Question one?\n2. Question two?'
        >>> extract_questions_after_think("1. Question one?\n2. Question two?")
        '1. Question one?\n2. Question two?'
        >>> extract_questions_after_think("   ")
        ''
    """
    if " response" in text:
        return text.split(" response", 1)[1].strip()
    return text.strip()