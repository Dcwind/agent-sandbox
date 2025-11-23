import os
from typing import Sequence

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.genai import types


def build_retry_config() -> types.HttpRetryOptions:
    return types.HttpRetryOptions(
        attempts=5,
        exp_base=7,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],
    )


def build_agent(
    *,
    model: str = "gemini-2.5-flash-lite",
    tools: Sequence = (google_search,),
) -> Agent:
    """
    Factory for the root agent. Keeps construction pure so it is easy to test and reuse.
    """
    if not os.getenv("GOOGLE_API_KEY"):
        raise EnvironmentError("GOOGLE_API_KEY must be set before building the agent.")

    return Agent(
        name="helpful_assistant",
        model=Gemini(model=model, retry_options=build_retry_config()),
        description="A simple agent that can answer general questions.",
        instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
        tools=list(tools),
    )
