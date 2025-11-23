# My ADK Agent

Run a simple Google ADK agent locally using `uv`.

## Quickstart
1) Install uv (if not present): `curl -LsSf https://astral.sh/uv/install.sh | sh`
2) Install deps (editable package + dev tools): `uv pip install -e .[dev]`
3) Set your key: `export GOOGLE_API_KEY=your_key_here`
4) Run: `uv run run-agent`

No uv? Use standard venv/pip: `python -m venv .venv && source .venv/bin/activate && pip install -e .[dev] && python -m my_adk_agent.run_agent`

## Formatting/Lint
- Format: `uv run ruff format`
- Lint: `uv run ruff check`
- Tests: `uv run pytest`

## Notes
- Agent lives in `src/my_adk_agent/agents/simple_agent.py`; runtime wiring in `src/my_adk_agent/run_agent.py`.
- Uses `Gemini` with `google_search` tool; change prompts inside `run_agent.py` or pass your own in code.
