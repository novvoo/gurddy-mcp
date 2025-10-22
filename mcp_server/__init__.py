"""
Gurddy MCP Server - Model Context Protocol server for optimization problems.

This package provides a complete MCP server implementation for solving
Constraint Satisfaction Problems (CSP), Linear Programming (LP), Game Theory,
and SciPy-powered advanced optimization problems using the Gurddy library.

Features:
- CSP: N-Queens, Graph/Map Coloring, Sudoku, Logic Puzzles, Scheduling
- LP/MIP: Linear Programming, Production Planning, Portfolio Optimization
- Game Theory: Minimax, Zero-Sum Games, Robust Optimization
- SciPy Integration: Nonlinear optimization, Statistical fitting, Signal processing
- Classic Problems: 24-point game, Chicken-rabbit, Mini sudoku, Knapsack
- Dual Transport: Stdio (IDE integration) and HTTP/SSE (web clients)
- Command-line tools and Python API

Usage:
    # As MCP stdio server (for IDE integration)
    gurddy-mcp

    # Run examples
    python -m mcp_server.server run-example minimax

    # HTTP API server
    uvicorn mcp_server.mcp_http_server:app --host 0.0.0.0 --port 8080

    # Direct import
    from mcp_server.handlers.gurddy import solve_minimax_game
    result = solve_minimax_game([[0, -1, 1], [1, 0, -1], [-1, 1, 0]], player="row")
"""

import importlib.metadata

try:
    __version__ = importlib.metadata.version("gurddy_mcp")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"  # Fallback for development

__author__ = "Gurddy MCP Team"
__email__ = "contact@example.com"

# Import tool registry for centralized tool management
from mcp_server.tool_registry import TOOLS, TOOL_COUNT
import importlib

# Dynamically import all registered functions from their respective modules
__all__ = []
for tool in TOOLS:
    func_name = tool["function"]
    module_path = f"mcp_server.{tool['module']}"
    
    try:
        module = importlib.import_module(module_path)
        if hasattr(module, func_name):
            globals()[func_name] = getattr(module, func_name)
            __all__.append(func_name)
    except ImportError:
        pass  # Skip if module doesn't exist

# Add solve_csp_generic if it exists (not in registry but useful)
try:
    _handler_module = importlib.import_module("mcp_server.handlers.gurddy")
    if hasattr(_handler_module, "solve_csp_generic"):
        solve_csp_generic = getattr(_handler_module, "solve_csp_generic")
        __all__.append("solve_csp_generic")
except ImportError:
    pass