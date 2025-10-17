"""Tool wrapper to run gurddy example scripts (lp / csp)."""
from __future__ import annotations

from mcp_server.handlers.gurddy import run_example


def run(args: dict) -> dict:
    example = args.get('example', 'lp')
    return run_example(example)
