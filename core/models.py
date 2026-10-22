"""Dataclasses shared across the services and UI layers."""

from dataclasses import dataclass


@dataclass
class QuestionAnswer:
    """A single research question paired with the agent's answer.

    Replaces the inline dict {"question": ..., "answer": ...} used in
    orig. line 206; attribute access (.question/.answer) is equivalent.
    """

    question: str
    answer: str