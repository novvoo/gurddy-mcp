"""Tool wrapper to install gurddy via pip (used by MCP)."""
from __future__ import annotations

from mcp_server.handlers.gurddy import pip_install


def run(args: dict) -> dict:
    package = args.get('package', 'gurddy')
    upgrade = args.get('upgrade', False)
    return pip_install(package, upgrade=upgrade)

