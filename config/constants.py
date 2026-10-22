"""Centralized hardcoded constants extracted from the original single-file app."""

# ---------------------------------------------------------------------------
# LLM model
# ---------------------------------------------------------------------------
# Alibaba Cloud Bailian (DashScope) model identifier used by all agents.
MODEL_ID = "qwen3-coder-flash"
# DashScope OpenAI-compatible endpoint (orig. line 68 used Together AI).
DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# ---------------------------------------------------------------------------
# Research parameters
# ---------------------------------------------------------------------------
# Number of yes/no research questions the generator must produce
# (orig. lines 88-89, 107).
NUM_QUESTIONS = 5

# ---------------------------------------------------------------------------
# Streamlit page configuration (orig. lines 14-19)
# ---------------------------------------------------------------------------
PAGE_TITLE = "AI DeepResearch Agent"
PAGE_ICON = "\U0001f50d"  # U+1F50D left-pointing magnifier emoji
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# ---------------------------------------------------------------------------
# Web search (tavily-python SDK)
# ---------------------------------------------------------------------------
# Number of results Tavily returns per search call (used by the research agent).
TAVILY_MAX_RESULTS = 5