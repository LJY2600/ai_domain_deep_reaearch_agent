"""Unit tests for agents.prompts — template formatting only, no LLM/tool mocks."""

from agents.prompts import (
    COMPILER_INSTRUCTIONS_TEMPLATE,
    QUESTION_GENERATOR_INSTRUCTIONS,
    RESEARCHER_INSTRUCTIONS_TEMPLATE,
)
from config.constants import NUM_QUESTIONS


class TestQuestionGeneratorInstructions:
    """The generator prompt must embed the configured question count."""

    def test_contains_num_questions_value(self) -> None:
        assert str(NUM_QUESTIONS) in QUESTION_GENERATOR_INSTRUCTIONS

    def test_preserves_original_constraint(self) -> None:
        assert "Respond ONLY with the text of the" in QUESTION_GENERATOR_INSTRUCTIONS
        assert "numbered list, and NOTHING ELSE." in QUESTION_GENERATOR_INSTRUCTIONS

    def test_no_unresolved_placeholder(self) -> None:
        assert "NUM_QUESTIONS" not in QUESTION_GENERATOR_INSTRUCTIONS
        assert "{" not in QUESTION_GENERATOR_INSTRUCTIONS


class TestResearcherInstructionsTemplate:
    """The researcher template must accept topic/domain/question."""

    def test_formats_without_error(self) -> None:
        text = RESEARCHER_INSTRUCTIONS_TEMPLATE.format(
            topic="Tariffs", domain="Economics", question="Does it help?"
        )
        assert "Tariffs" in text
        assert "Economics" in text
        assert "Does it help?" in text

    def test_keeps_tool_hint(self) -> None:
        assert "tavily_search" in RESEARCHER_INSTRUCTIONS_TEMPLATE
        assert "tavily_search" in RESEARCHER_INSTRUCTIONS_TEMPLATE


class TestCompilerInstructionsTemplate:
    """The compiler template must render the McKinsey structure."""

    def test_formats_without_error(self) -> None:
        text = COMPILER_INSTRUCTIONS_TEMPLATE.format(
            topic="Tariffs", domain="Economics", qa_sections="<p>QA</p>"
        )
        assert "Tariffs" in text
        assert "Economics" in text
        assert "<p>QA</p>" in text

    def test_keeps_mckinsey_sections(self) -> None:
        for heading in (
            "Executive Summary/Introduction",
            "Research Analysis",
            "Conclusion/Implications",
        ):
            assert heading in COMPILER_INSTRUCTIONS_TEMPLATE

    def test_keeps_google_docs_hint(self) -> None:
        assert "GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN" in COMPILER_INSTRUCTIONS_TEMPLATE