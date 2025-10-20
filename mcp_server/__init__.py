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

__version__ = "0.1.6"
__author__ = "Gurddy MCP Team"
__email__ = "contact@example.com"

# Import main components for easy access
from mcp_server.handlers.gurddy import (
    solve_n_queens,
    solve_graph_coloring,
    solve_map_coloring,
    solve_sudoku,
    solve_lp,
    solve_csp_generic,
    solve_production_planning,
    solve_minimax_game,
    solve_minimax_decision,
    info,
    run_example,
)

__all__ = [
    "solve_n_queens",
    "solve_graph_coloring", 
    "solve_map_coloring",
    "solve_sudoku",
    "solve_lp",
    "solve_csp_generic",
    "solve_production_planning",
    "solve_minimax_game",
    "solve_minimax_decision",
    "info",
    "run_example",
]