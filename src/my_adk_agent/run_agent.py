import argparse
import asyncio
import os
import sys
import time
from typing import Iterable

from google.adk.runners import InMemoryRunner

from my_adk_agent.agents import build_agent


def _extract_text(response: object) -> str:
    """
    Try to extract a human-friendly text reply from an ADK response/event.
    Falls back to repr(response) if no known attributes are present.
    """
    # Gemini responses often expose .text directly.
    text = getattr(response, "text", None)
    if isinstance(text, str) and text.strip():
        return text

    # ADK events commonly have .content.parts with .text fields.
    content = getattr(response, "content", None)
    parts = getattr(content, "parts", None) if content else None
    if parts:
        texts = [getattr(p, "text", "") for p in parts if getattr(p, "text", "")]
        if texts:
            return "\n".join(texts)

    return repr(response)


def _validate_env() -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        sys.exit("Set GOOGLE_API_KEY in your environment before running this script.")
    os.environ["GOOGLE_API_KEY"] = api_key
    return api_key


async def run_prompts(prompts: Iterable[str]) -> None:
    _validate_env()
    agent = build_agent()
    runner = InMemoryRunner(agent=agent, app_name="my_adk_agent")

    for prompt in prompts:
        print(f"\n>>> {prompt}")
        start = time.monotonic()
        try:
            response = await runner.run_debug(prompt)
        except Exception as exc:  # broad by design to surface ADK errors
            duration = time.monotonic() - start
            print(f"Error after {duration:.2f}s: {exc}")
            continue
        duration = time.monotonic() - start
        print(f"(completed in {duration:.2f}s)")
        print(_extract_text(response))


async def _async_main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the ADK agent with one or more prompts."
    )
    parser.add_argument(
        "prompts",
        nargs="+",
        help="Prompt(s) to send to the agent. Provide multiple to run sequentially.",
    )
    args = parser.parse_args()
    await run_prompts(args.prompts)


def main() -> None:
    asyncio.run(_async_main())


if __name__ == "__main__":
    main()
