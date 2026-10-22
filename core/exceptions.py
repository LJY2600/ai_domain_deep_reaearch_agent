"""Custom exception hierarchy for the deep research app."""


class DeepResearchError(Exception):
    """Base class for all application-specific errors."""


class AgentInitError(DeepResearchError):
    """Raised when LLM or Composio tool initialization fails."""


class ResearchError(DeepResearchError):
    """Raised when researching a single question fails."""


class CompileError(DeepResearchError):
    """Raised when report compilation or Google Doc creation fails."""


class ParseError(DeepResearchError):
    """Raised when model output cannot be parsed into the expected structure."""