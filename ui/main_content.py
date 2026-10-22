"""Main content area: research topic inputs and the three action buttons."""

import streamlit as st

# Widget keys must match ai_domain_deep_research_agent.py exactly
# (orig. lines 180, 190, 222).
KEY_GENERATE_QUESTIONS: str = "generate_questions"
KEY_START_RESEARCH: str = "start_research"
KEY_COMPILE_REPORT: str = "compile_report"

TOPIC_PLACEHOLDER: str = "American Tariffs"
DOMAIN_PLACEHOLDER: str = "Politics, Economics, Technology, etc."


def render_inputs() -> tuple[str, str, bool]:
    """Render the topic/domain inputs and the generate button (orig. 170-180).

    Returns:
        (topic, domain, generate_clicked). The button is only rendered once both
        fields are non-empty, exactly like the original short-circuited
        ``if topic and domain and st.button(...)``.
    """
    st.header("Research Topic")

    col1, col2 = st.columns(2)
    with col1:
        topic: str = st.text_input(
            "What topic would you like to research?", placeholder=TOPIC_PLACEHOLDER
        )
    with col2:
        domain: str = st.text_input(
            "What domain is this topic in?", placeholder=DOMAIN_PLACEHOLDER
        )

    generate_clicked: bool = False
    if topic and domain:
        generate_clicked = st.button(
            "Generate Research Questions", key=KEY_GENERATE_QUESTIONS
        )

    return topic, domain, generate_clicked


def render_research_button() -> bool:
    """Render the "Start Research" button and return whether it was clicked."""
    return bool(st.button("Start Research", key=KEY_START_RESEARCH))


def render_compile_button() -> bool:
    """Render the "Compile Final Report" button and return whether it was clicked.

    Must be called from the top level of the script run - never nested inside
    the research block (see the warning at orig. lines 219-221).
    """
    return bool(st.button("Compile Final Report", key=KEY_COMPILE_REPORT))
