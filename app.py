"""Application entry point: orchestration only, no business logic.

Wires ui/ (rendering), services/ (agent orchestration), agents/factory.py
(cached resource construction) and core/state.py (session state) together,
mirroring the control flow of ai_domain_deep_research_agent.py lines 164-273.
"""

import logging

import streamlit as st

from agents.factory import build_search_tools, get_llm
from config.constants import INITIAL_SIDEBAR_STATE, LAYOUT, PAGE_ICON, PAGE_TITLE
from config.settings import Settings, validate_settings
from core.models import QuestionAnswer
from core.state import SessionState
from services.research_service import (
    compile_report,
    generate_questions,
    research_question,
)
from ui.main_content import (
    render_compile_button,
    render_inputs,
    render_research_button,
)
from ui.renderers import (
    render_answer,
    render_final_report,
    render_progress,
    render_question_list,
    render_welcome,
)
from ui.sidebar import render_sidebar

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Orig. line 63: rendered before the key check so both branches show it.
MAIN_TITLE: str = "🔍 AI DeepResearch Agent with Agno and Tavily"
# Placeholder stored when a single question cannot be researched.
RESEARCH_FAILED_ANSWER: str = "_Research failed for this question._"

# Orig. lines 14-19 - must be the first Streamlit call of the script run.
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state=INITIAL_SIDEBAR_STATE,
)
# Orig. lines 53-60.
SessionState.init()


def _research_all(
    llm, tools, questions: list[str], topic: str, domain: str
) -> list[QuestionAnswer]:
    """Research every question, warning (never aborting) on per-question failure."""
    total: int = len(questions)
    answers: list[QuestionAnswer] = []
    progress_slot = st.empty()

    for index, question in enumerate(questions):
        with progress_slot.container():
            render_progress(index, total)

        try:
            with st.spinner(f"🔍 Researching question {index + 1}..."):
                qa = research_question(llm, tools, topic, domain, question)
        except Exception as exc:  # noqa: BLE001 - one bad question must not stop the run
            logger.exception("research_question failed for question %d", index + 1)
            st.warning(f"⚠️ Question {index + 1} could not be researched: {exc}")
            qa = QuestionAnswer(question=question, answer=RESEARCH_FAILED_ANSWER)

        answers.append(qa)
        render_answer(index + 1, qa.question, qa.answer)

        with progress_slot.container():
            render_progress(index + 1, total)

    return answers


def main() -> None:
    """Render one Streamlit script run."""
    # 2. Sidebar: collect both API keys (orig. lines 22-50).
    dashscope_api_key, tavily_api_key = render_sidebar()

    st.title(MAIN_TITLE)

    # 3. Validate keys (orig. line 165 / lines 255-273).
    is_valid, message = validate_settings(
        Settings(dashscope_api_key=dashscope_api_key, tavily_api_key=tavily_api_key)
    )
    if not is_valid:
        logger.warning("API key validation failed: %s", message)
        render_welcome()
        st.stop()

    # 4. Cached LLM + Tavily search tools.
    try:
        llm = get_llm(dashscope_api_key)
        tools = build_search_tools(tavily_api_key)
    except Exception as exc:  # noqa: BLE001 - surface init failure instead of crashing
        logger.exception("Resource initialization failed")
        st.error(f"❌ Failed to initialize the AI resources: {exc}")
        st.stop()
        return

    # 5. Inputs (orig. lines 170-180).
    topic, domain, generate_clicked = render_inputs()

    # 6. Generate questions.
    if topic and domain and generate_clicked:
        try:
            new_questions = generate_questions(llm, topic, domain)
        except Exception as exc:  # noqa: BLE001
            logger.exception("generate_questions failed")
            st.error(f"❌ Failed to generate research questions: {exc}")
        else:
            SessionState.set("questions", new_questions)
            SessionState.set("topic", topic)
            SessionState.set("domain", domain)
            render_question_list(new_questions)

    # Topic/domain the stored questions were generated for; persisted so the
    # research and compile reruns stay consistent with those questions.
    active_topic: str = SessionState.get("topic") or topic
    active_domain: str = SessionState.get("domain") or domain

    # 7. Research branch (orig. lines 190-217).
    questions: list[str] = SessionState.get("questions") or []
    if questions and render_research_button():
        st.header("Research Results")
        SessionState.set(
            "question_answers",
            _research_all(llm, tools, questions, active_topic, active_domain),
        )

    # Re-read so the run that just finished researching sees its own results.
    stored_answers: list[QuestionAnswer] = SessionState.get("question_answers") or []

    # 8. Compile branch - deliberately NOT nested inside the research block.
    # Orig. lines 219-222: clicking this button reruns the script, at which
    # point "Start Research" is False, so a nested button would never render
    # and could therefore never fire.
    report_rendered = False
    if stored_answers and render_compile_button():
        try:
            with st.spinner("📝 Compiling final report and creating Google Doc..."):
                report_content = compile_report(
                    llm, tools, active_topic, active_domain, stored_answers
                )
        except Exception as exc:  # noqa: BLE001
            logger.exception("compile_report failed")
            st.error(f"❌ Failed to compile the final report: {exc}")
        else:
            SessionState.set("report_content", report_content)
            SessionState.set("research_complete", True)
            render_final_report(report_content)
            report_rendered = True

    # 9. Previous results (orig. lines 236-242).
    if stored_answers and not SessionState.get("research_complete"):
        st.header("Previous Research Results")
        for index, qa in enumerate(stored_answers):
            with st.expander(f"Question {index + 1}: {qa.question}"):
                st.markdown(qa.answer)

    # 10. Final report from an earlier run (orig. lines 245-253). The flag
    # keeps the report from being rendered twice in the run that compiled it.
    if (
        SessionState.get("research_complete")
        and SessionState.get("report_content")
        and not report_rendered
    ):
        render_final_report(SessionState.get("report_content"))


if __name__ == "__main__":
    main()
