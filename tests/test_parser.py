"""Unit tests for core.parser module."""

import pytest

from core.parser import extract_questions_after_think


class TestExtractQuestionsAfterThink:
    """Tests for extract_questions_after_think."""

    def test_extracts_content_after_response_marker(self) -> None:
        """Content after ' response' should be returned stripped."""
        text = " response1. Is this a question?\n2. Is this another?"
        result = extract_questions_after_think(text)
        assert result == "1. Is this a question?\n2. Is this another?"

    def test_returns_full_text_when_no_response_marker(self) -> None:
        """When ' response' is absent, return original text stripped."""
        text = "1. Question one?\n2. Question two?\n3. Question three?"
        result = extract_questions_after_think(text)
        assert result == "1. Question one?\n2. Question two?\n3. Question three?"

    def test_handles_empty_string(self) -> None:
        """Empty input should return empty string."""
        result = extract_questions_after_think("")
        assert result == ""

    def test_handles_only_whitespace(self) -> None:
        """Whitespace-only input should return empty string."""
        result = extract_questions_after_think("   \n\t  ")
        assert result == ""

    def test_response_marker_at_start(self) -> None:
        """When ' response' is at the very beginning."""
        text = " responsehello world"
        result = extract_questions_after_think(text)
        assert result == "hello world"

    def test_response_marker_appears_multiple_times(self) -> None:
        """Only the first ' response' occurrence is used as split point."""
        text = " responsefirst responsesecond responsethird"
        result = extract_questions_after_think(text)
        assert result == "first responsesecond responsethird"

    def test_response_without_leading_space_not_marker(self) -> None:
        """'response' without leading space is NOT treated as marker."""
        text = "myresponse is not a delimiter here"
        result = extract_questions_after_think(text)
        assert result == "myresponse is not a delimiter here"

    def test_think_is_not_a_marker(self) -> None:
        """' think' alone is NOT treated as delimiter — only ' response' is."""
        text = " think this should not be split"
        result = extract_questions_after_think(text)
        # .strip() removes leading space from result
        assert result == "think this should not be split"