"""Streamlit session_state wrapper — the only core module allowed to import streamlit.

Used exclusively by ui/ and app.py. services/ must never import this module.
"""

from typing import Any

import streamlit as st

# Defaults extracted from orig. lines 53-60. topic/domain are new: the original
# relied on widget return values living in one script run's scope, so they are
# persisted here for the compile step.
DEFAULT_KEYS: dict[str, Any] = {
    "questions": [],
    "question_answers": [],
    "report_content": "",
    "research_complete": False,
    "topic": "",
    "domain": "",
}

# Result keys cleared by reset_research(); inputs (topic/domain, API keys) kept.
_RESULT_KEYS: tuple[str, ...] = (
    "questions",
    "question_answers",
    "report_content",
    "research_complete",
)


class SessionState:
    """Typed accessor layer over st.session_state for the research app."""

    @classmethod
    def init(cls) -> None:
        """Set a default value for every key that is still missing.

        Mirrors orig. lines 53-60. Mutable defaults are shallow-copied so each
        session owns its own list instance.
        """
        for key, value in DEFAULT_KEYS.items():
            if key not in st.session_state:
                st.session_state[key] = list(value) if isinstance(value, list) else value

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Read one session_state value, falling back to *default*."""
        return st.session_state.get(key, default)

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """Write one session_state value."""
        st.session_state[key] = value

    @classmethod
    def reset_research(cls) -> None:
        """Clear research results while preserving inputs and API keys.

        Resets questions/question_answers/report_content/research_complete to
        their defaults; leaves topic/domain untouched.
        """
        for key in _RESULT_KEYS:
            value = DEFAULT_KEYS[key]
            st.session_state[key] = list(value) if isinstance(value, list) else value