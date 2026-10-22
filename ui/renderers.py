"""Reusable Streamlit output components: questions, progress, answers, report."""

import streamlit as st


def render_question_list(questions: list[str]) -> None:
    """Display the generated research questions (orig. lines 185-187)."""
    st.header("Research Questions")
    for index, question in enumerate(questions):
        st.markdown(f"**{index + 1}. {question}**")


def render_progress(current: int, total: int) -> None:
    """Render the research progress bar for *current* of *total* questions.

    Call it inside an ``st.empty()`` slot to make the bar advance in place
    (orig. lines 197-214 used a stored ``st.progress`` handle).
    """
    if total <= 0:
        st.progress(0.0, text="Waiting for questions...")
        return
    fraction: float = min(1.0, max(0.0, current / total))
    st.progress(fraction, text=f"Researching question {min(current + 1, total)} of {total}")


def render_answer(index: int, question: str, answer: str) -> None:
    """Display one researched question/answer pair (orig. lines 209-211)."""
    st.subheader(f"Question {index}:")
    st.markdown(f"**{question}**")
    st.markdown(answer)


def render_final_report(content: str) -> None:
    """Display the compiled report (orig. lines 228-233 and 245-253)."""
    st.header("Final Report")
    st.success("Your report has been compiled and a Google Doc has been created.")
    with st.expander("View Full Report Content", expanded=True):
        st.markdown(content)


def render_welcome() -> None:
    """Render the API-key-missing guide page (orig. lines 257-273)."""
    st.warning(
        "⚠️ Please enter your Together AI and Composio API keys "
        "in the sidebar to get started."
    )

    st.header("How It Works")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("1️⃣ Define Topic")
        st.write("Enter your research topic and domain to begin the research process.")

    with col2:
        st.subheader("2️⃣ Generate Questions")
        st.write("The AI generates specific research questions to explore your topic in depth.")

    with col3:
        st.subheader("3️⃣ Compile Report")
        st.write(
            "Research findings are compiled into a professional report "
            "and saved to Google Docs."
        )
