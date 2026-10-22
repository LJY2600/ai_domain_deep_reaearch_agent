"""Sidebar rendering: API key inputs plus the static About / Tools panel."""

import streamlit as st

from config.settings import Settings, get_settings

# Static sidebar copy (orig. lines 42-50).
ABOUT_TEXT: str = (
    "This AI DeepResearch Agent uses Qwen model (via DashScope) and Tavily search to perform comprehensive research on any topic.It generates research questions, finds answers, and compiles aprofessional report."
)
TOOLS_USED: tuple[str, ...] = (
    "- 🔍 Tavily Search",
)


def render_sidebar() -> tuple[str, str]:
    """Render the configuration sidebar (orig. lines 22-50).

    Returns:
        (dashscope_api_key, tavily_api_key) exactly as typed by the user,
        pre-filled from config.settings.get_settings().
    """
    settings: Settings = get_settings()

    st.sidebar.header("⚙️ Configuration")

    dashscope_api_key: str = st.sidebar.text_input(
        "DashScope API Key",
        value=settings.dashscope_api_key,
        type="password",
        help="Get your API key from https://bailian.console.aliyun.com",
    )

    tavily_api_key: str = st.sidebar.text_input(
        "Tavily API Key",
        value=settings.tavily_api_key,
        type="password",
        help="Get your API key from https://tavily.com",
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(ABOUT_TEXT)

    st.sidebar.markdown("### Tools Used")
    for tool_line in TOOLS_USED:
        st.sidebar.markdown(tool_line)

    return dashscope_api_key, tavily_api_key
