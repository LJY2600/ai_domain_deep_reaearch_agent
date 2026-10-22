
from unittest.mock import MagicMock

from core.models import QuestionAnswer
from services.research_service import compile_report


RESEARCH_FAILED_ANSWER = "_Research failed for this question._"


def test_compile_report_excludes_failed_answers(monkeypatch) -> None:
    """编译报告时跳过失败答案，并保留成功答案。"""
    question_answers = [
        QuestionAnswer(question="问题 A", answer="答案 A"),
        QuestionAnswer(
            question="问题 B",
            answer=RESEARCH_FAILED_ANSWER,
        ),
        QuestionAnswer(question="问题 C", answer="答案 C"),
    ]

    captured = {}

    class FakeAgent:
        def run(self, prompt):
            captured["prompt"] = prompt
            return MagicMock(content="编译后的报告")

    def fake_build_compiler(llm, tools, topic, domain, qa_sections):
        captured["qa_sections"] = qa_sections
        return FakeAgent()

    monkeypatch.setattr(
        "services.research_service.build_compiler",
        fake_build_compiler,
    )

    original_answers = question_answers.copy()

    result = compile_report(
        llm=None,
        tools=[],
        topic="测试主题",
        domain="测试领域",
        question_answers=question_answers,
    )

    assert result == "编译后的报告"
    assert "问题 A" in captured["qa_sections"]
    assert "答案 A" in captured["qa_sections"]
    assert "问题 B" not in captured["qa_sections"]
    assert RESEARCH_FAILED_ANSWER not in captured["qa_sections"]
    assert "问题 C" in captured["qa_sections"]
    assert "答案 C" in captured["qa_sections"]
    assert question_answers == original_answers
    assert captured["prompt"] == captured["qa_sections"]
