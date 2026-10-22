"""Environment-based settings loaded once at import time."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load environment variables from a local .env file (orig. line 11).
load_dotenv()


@dataclass
class Settings:
    """API keys required to run the research agents."""

    dashscope_api_key: str
    tavily_api_key: str


def get_settings() -> Settings:
    """Read API keys from the environment, defaulting to empty strings.

    Returns:
        A Settings instance populated from DASHSCOPE_API_KEY / TAVILY_API_KEY.
    """
    return Settings(
        dashscope_api_key=os.getenv("DASHSCOPE_API_KEY", ""),
        tavily_api_key=os.getenv("TAVILY_API_KEY", ""),
    )


def validate_settings(settings: Settings) -> tuple[bool, str]:
    """Check that both API keys are present.

    Mirrors orig. line 165: the app only runs when both keys are non-empty.

    Args:
        settings: The Settings instance to validate.

    Returns:
        (True, "") if both keys are non-empty; otherwise (False, message).
    """
    if not settings.dashscope_api_key or not settings.tavily_api_key:
        return (
            False,
            "Please enter your DashScope (Alibaba Cloud Bailian) and Tavily "
            "API keys in the sidebar to get started.",
        )
    return (True, "")