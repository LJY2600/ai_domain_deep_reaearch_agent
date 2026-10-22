"""Agent, LLM, and tool factories — construction only, never calls run().

Web search is provided by the official tavily-python SDK. Agno accepts plain
Python callables as agent tools, so build_search_tools() simply returns the
tavily_search function in a list.
"""

import logging
from typing import Any

import streamlit as st
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from tavily import TavilyClient

from agents.prompts import (
    COMPILER_INSTRUCTIONS_TEMPLATE,
    QUESTION_GENERATOR_INSTRUCTIONS,
    RESEARCHER_INSTRUCTIONS_TEMPLATE,
)
from config.constants import DASHSCOPE_BASE_URL, MODEL_ID, TAVILY_MAX_RESULTS

logger = logging.getLogger(__name__)


@st.cache_resource
def get_llm(dashscope_api_key: str) -> OpenAILike:
    """Create (and cache) the DashScope LLM client via its OpenAI-compatible API."""
    return OpenAILike(
        id=MODEL_ID,
        api_key=dashscope_api_key,
        base_url=DASHSCOPE_BASE_URL,
    )


@st.cache_resource
def get_tavily_client(tavily_api_key: str) -> TavilyClient:
    """Create (and cache) the Tavily search client for the given API key."""
    return TavilyClient(api_key=tavily_api_key)


def build_search_tools(tavily_api_key: str) -> list[Any]:
    """Build the agent tool list backed by the Tavily Search API.

    Args:
        tavily_api_key: API key used to authenticate the cached Tavily client.

    Returns:
        A list holding the single ``tavily_search`` callable, ready to be passed
        to ``Agent(tools=...)``.
    """
    client: TavilyClient = get_tavily_client(tavily_api_key)

    def tavily_search(query: str) -> str:
        """Search the web with Tavily and return the top results as readable text.

        Args:
            query: Natural-language search query.

        Returns:
            A numbered list of "title / URL / snippet" blocks, an explicit
            "no results" note, or an error message if the request failed.
        """
        try:
            response: dict[str, Any] = client.search(
                query, max_results=TAVILY_MAX_RESULTS
            )
        except Exception as exc:  # noqa: BLE001 - a failed search must not crash the agent
            logger.exception("tavily_search failed for query: %s", query[:80])
            return f"Tavily search failed: {exc}"

        results: list[dict[str, Any]] = response.get("results") or []
        if not results:
            return f"No search results found for: {query}"

        blocks: list[str] = []
        for index, item in enumerate(results, start=1):
            title: str = str(item.get("title") or "Untitled")
            url: str = str(item.get("url") or "")
            content: str = str(item.get("content") or "").strip()
            blocks.append(f"{index}. {title}\nURL: {url}\n{content}")
        return "\n\n".join(blocks)

    return [tavily_search]


def build_question_generator(llm: OpenAILike) -> Agent:
    """Build the question generator agent (orig. lines 83-91)."""
    return Agent(
        name="Question Generator",
        model=llm,
        instructions=QUESTION_GENERATOR_INSTRUCTIONS,
    )


def build_researcher(
    llm: OpenAILike, tools: list[Any], topic: str, domain: str, question: str
) -> Agent:
    """Build a per-question research agent (orig. lines 119-123).

    Fixes the original bug that wrapped the tool list in another list
    (tools=[composio_tools]); the list is now passed directly.
    """
    return Agent(
        model=llm,
        tools=tools,
        instructions=RESEARCHER_INSTRUCTIONS_TEMPLATE.format(
            topic=topic, domain=domain, question=question
        ),
    )


def build_compiler(
    llm: OpenAILike, tools: list[Any], topic: str, domain: str, qa_sections: str
) -> Agent:
    """Build the report compiler agent (orig. lines 136-157)."""
    return Agent(
        name="Report Compiler",
        model=llm,
        tools=tools,
        instructions=COMPILER_INSTRUCTIONS_TEMPLATE.format(
            topic=topic, domain=domain, qa_sections=qa_sections
        ),
    )