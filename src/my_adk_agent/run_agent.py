import asyncio
import os
import sys
import time
from typing import Iterable

from google.adk.runners import InMemoryRunner

from my_adk_agent.agents import build_agent


def _validate_env() -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        sys.exit("Set GOOGLE_API_KEY in your environment before running this script.")
    os.environ["GOOGLE_API_KEY"] = api_key
    return api_key


async def run_prompts(prompts: Iterable[str]) -> None:
    _validate_env()
    agent = build_agent()
    runner = InMemoryRunner(agent=agent)

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
        print(response)


async def _async_main() -> None:
    prompts = (
        "What is Agent Development Kit from Google? What languages is the SDK available in?",
        "What's the current time in Stockholm?",
    )
    await run_prompts(prompts)


def main() -> None:
    asyncio.run(_async_main())


if __name__ == "__main__":
    main()
