"""Research orchestration service — builds agents, runs them, catches & wraps errors.

Replaces the monolithic functions in ai_domain_deep_research_agent.py lines 102-162.
No Streamlit dependency; UI concerns are handled by ui/.
"""

import logging
from typing import Any

from agents.factory import build_compiler, build_question_generator, build_researcher
from core.exceptions import CompileError, ParseError, ResearchError
from core.parser import extract_questions_after_think
from core.models import QuestionAnswer

logger = logging.getLogger(__name__)


def generate_questions(llm, topic: str, domain: str) -> list[str]:
    """Generate NUM_QUESTIONS yes/no research questions (orig. lines 102-115)."""
    logger.info("generate_questions called: topic=%s, domain=%s", topic, domain)
    try:
        agent = build_question_generator(llm)
        result: Any = agent.run(f"Generate exactly 5 specific yes/no "
                                      f"research questions about the topic '{topic}' "
                                      f"in the domain '{domain}'.")
        questions_text = result.content
        questions_only = extract_questions_after_think(questions_text)
        questions_list = [q.strip() for q in questions_only.split("\n") if q.strip()]
        if not questions_list:
            raise ParseError("LLM returned no parseable questions")
        logger.info("generate_questions completed: %d questions extracted", len(questions_list))
        return questions_list
    except (ParseError, ValueError):
        raise
    except Exception as exc:
        logger.exception("generate_questions failed")
        raise ParseError(str(exc)) from exc


def research_question(llm, tools, topic: str, domain: str, question: str) -> QuestionAnswer:
    """Research a single question and return a QuestionAnswer object (orig. lines 118-126)."""
    logger.info("research_question called: topic=%s, domain=%s, question=%s",
                topic, domain, question[:80])
    try:
        agent = build_researcher(llm, tools, topic, domain, question)
        result: Any = agent.run(question)
        answer = result.content
        logger.info("research_question completed successfully")
        return QuestionAnswer(question=question, answer=str(answer))
    except Exception as exc:
        logger.exception("research_question failed")
        raise ResearchError(str(exc)) from exc


def compile_report(llm, tools, topic: str, domain: str,
                   question_answers: list[QuestionAnswer]) -> str:
    """Compile findings into McKinsey-style report HTML (orig. lines 129-162)."""
    logger.info("compile_report called: topic=%s, domain=%s, n_findings=%d",
                topic, domain, len(question_answers))
    try:
        successful_answers = [
            qa for qa in question_answers
            if qa.answer != "_Research failed for this question._"
        ]

        qa_sections = "\n".join(
            f"<h2>{idx + 1}. {qa.question}</h2>\n<p>{qa.answer}</p>"
            for idx, qa in enumerate(successful_answers)
        )
        
        agent = build_compiler(llm, tools, topic, domain, qa_sections)
        result: Any = agent.run(qa_sections)
        logger.info("compile_report completed successfully")
        return result.content
    except Exception as exc:
        logger.exception("compile_report failed")
        raise CompileError(str(exc)) from exc