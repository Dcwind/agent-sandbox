from my_adk_agent.agents import build_agent


def test_agent_builds(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "dummy-key")
    agent = build_agent()
    assert agent.name == "helpful_assistant"
    assert agent.tools  # ensure at least one tool is registered
