"""
Gurddy MCP Server - Model Context Protocol server for optimization problems.

This package provides a complete MCP server implementation for solving
Constraint Satisfaction Problems (CSP) and Linear Programming (LP) problems
using the Gurddy optimization library.

Features:
- N-Queens problem solving
- Graph coloring algorithms
- Map coloring problems
- Scheduling optimization
- Logic puzzles (including Einstein's Zebra puzzle)
- Sudoku solver
- Linear programming optimization
- Production planning
- HTTP API interface
- Command-line tools

Usage:
    # As MCP server
    python -m mcp_server.server

    # Run examples
    python -m mcp_server.server run-example n_queens

    # HTTP API server
    uvicorn mcp_server.http_api:app --host 0.0.0.0 --port 8080

    # Direct import
    from mcp_server.handlers.gurddy import solve_n_queens
    result = solve_n_queens(8)
"""

__version__ = "0.1.0"
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
    "info",
    "run_example",
]