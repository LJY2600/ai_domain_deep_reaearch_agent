"""Unit tests for agents.factory (Tavily tools) and config.settings — no network."""

from typing import Any

import agents.factory as factory
from config.constants import TAVILY_MAX_RESULTS
from config.settings import Settings, get_settings, validate_settings


class FakeTavilyClient:
    """Stand-in for tavily.TavilyClient: records calls, returns canned data."""

    def __init__(
        self,
        response: dict[str, Any] | None = None,
        error: Exception | None = None,
    ) -> None:
        self.response: dict[str, Any] = {"results": []} if response is None else response
        self.error: Exception | None = error
        self.calls: list[tuple[str, int]] = []

    def search(self, query: str, max_results: int = 5) -> dict[str, Any]:
        self.calls.append((query, max_results))
        if self.error is not None:
            raise self.error
        return self.response


def _install_client(monkeypatch: Any, client: FakeTavilyClient) -> None:
    """Route build_search_tools() at the fake client instead of the Tavily API."""
    monkeypatch.setattr(factory, "get_tavily_client", lambda api_key: client)


class TestBuildSearchTools:
    """build_search_tools must expose one plain-Python Agno tool."""

    def test_returns_single_callable_named_tavily_search(self, monkeypatch: Any) -> None:
        _install_client(monkeypatch, FakeTavilyClient())
        tools = factory.build_search_tools("tvly-test")
        assert isinstance(tools, list)
        assert len(tools) == 1
        assert callable(tools[0])
        assert tools[0].__name__ == "tavily_search"

    def test_formats_results_as_string(self, monkeypatch: Any) -> None:
        client = FakeTavilyClient(
            response={
                "results": [
                    {"title": "First", "url": "https://a.example", "content": "Snippet A"},
                    {"title": "Second", "url": "https://b.example", "content": "Snippet B"},
                ]
            }
        )
        _install_client(monkeypatch, client)
        output = factory.build_search_tools("tvly-test")[0]("tariffs")

        assert isinstance(output, str)
        assert "1. First" in output
        assert "URL: https://a.example" in output
        assert "Snippet A" in output
        assert "2. Second" in output
        assert "Snippet B" in output

    def test_passes_configured_max_results(self, monkeypatch: Any) -> None:
        client = FakeTavilyClient()
        _install_client(monkeypatch, client)
        factory.build_search_tools("tvly-test")[0]("tariffs")
        assert client.calls == [("tariffs", TAVILY_MAX_RESULTS)]

    def test_missing_fields_do_not_crash(self, monkeypatch: Any) -> None:
        client = FakeTavilyClient(response={"results": [{"content": "Only content"}]})
        _install_client(monkeypatch, client)
        output = factory.build_search_tools("tvly-test")[0]("q")
        assert "Untitled" in output
        assert "Only content" in output

    def test_empty_results_message(self, monkeypatch: Any) -> None:
        _install_client(monkeypatch, FakeTavilyClient(response={"results": []}))
        output = factory.build_search_tools("tvly-test")[0]("nothing")
        assert output == "No search results found for: nothing"

    def test_missing_results_key_message(self, monkeypatch: Any) -> None:
        _install_client(monkeypatch, FakeTavilyClient(response={}))
        assert "No search results found for:" in factory.build_search_tools("k")[0]("q")

    def test_search_error_is_returned_not_raised(self, monkeypatch: Any) -> None:
        client = FakeTavilyClient(error=RuntimeError("401 unauthorized"))
        _install_client(monkeypatch, client)
        output = factory.build_search_tools("tvly-test")[0]("tariffs")
        assert output.startswith("Tavily search failed:")
        assert "401 unauthorized" in output


class TestGetTavilyClient:
    """The client factory must be cached and hand the key to the SDK."""

    def test_returns_tavily_client_instance(self) -> None:
        from tavily import TavilyClient

        client = factory.get_tavily_client("tvly-test")
        assert isinstance(client, TavilyClient)
        assert client.api_key == "tvly-test"

    def test_same_key_returns_cached_instance(self) -> None:
        assert factory.get_tavily_client("tvly-cache") is factory.get_tavily_client(
            "tvly-cache"
        )


class TestSettings:
    """Settings must carry the DashScope and Tavily keys."""

    def test_get_settings_reads_environment(self, monkeypatch: Any) -> None:
        monkeypatch.setenv("DASHSCOPE_API_KEY", "ds-key")
        monkeypatch.setenv("TAVILY_API_KEY", "tvly-key")
        settings = get_settings()
        assert settings.dashscope_api_key == "ds-key"
        assert settings.tavily_api_key == "tvly-key"

    def test_get_settings_defaults_to_empty(self, monkeypatch: Any) -> None:
        monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
        monkeypatch.delenv("TAVILY_API_KEY", raising=False)
        settings = get_settings()
        assert settings == Settings(dashscope_api_key="", tavily_api_key="")

    def test_validate_settings_accepts_both_keys(self) -> None:
        assert validate_settings(Settings("ds", "tvly")) == (True, "")

    def test_validate_settings_rejects_missing_keys(self) -> None:
        for settings in (Settings("", "tvly"), Settings("ds", ""), Settings("", "")):
            is_valid, message = validate_settings(settings)
            assert is_valid is False
            assert "DashScope" in message
            assert "Tavily" in message
