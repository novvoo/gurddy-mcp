"""
Tool definitions - only basic metadata, schemas auto-generated from functions.
This is the single source of truth for tool metadata.
"""

from typing import List, Dict, Any

# Basic tool definitions - schemas will be auto-generated
TOOL_DEFINITIONS = [
    {
        "name": "info",
        "function": "info",
        "description": "Get information about the gurddy package",
        "category": "meta",
        "module": "handlers.gurddy"
    },
    {
        "name": "install",
        "function": "pip_install",
        "description": "Install or upgrade the gurddy package",
        "category": "meta",
        "module": "handlers.gurddy"
    },
    {
        "name": "run_example",
        "function": "run_example",
        "description": "Run a gurddy example (lp, csp, n_queens, graph_coloring, map_coloring, scheduling, logic_puzzles, optimized_csp, optimized_lp, minimax, scipy_optimization, classic_problems)",
        "category": "examples",
        "module": "handlers.gurddy"
    },
    {
        "name": "solve_n_queens",
        "function": "solve_n_queens",
        "description": "Solve the N-Queens problem",
        "category": "csp",
        "module": "handlers.gurddy"
    },
    {
        "name": "solve_sudoku",
        "function": "solve_sudoku",
        "description": "Solve a 9x9 Sudoku puzzle",
        "category": "csp",
        "module": "handlers.gurddy"
    },
    {
        "name": "solve_graph_coloring",
        "function": "solve_graph_coloring",
        "description": "Solve graph coloring problem",
        "category": "csp",
        "module": "handlers.gurddy"
    },
    {
        "name": "solve_map_coloring",
        "function": "solve_map_coloring",
        "description": "Solve map coloring problem",
        "category": "csp",
        "module": "handlers.gurddy"
    },
    {
        "name": "solve_lp",
        "function": "solve_lp",
        "description": "Solve a Linear Programming (LP) or Mixed Integer Programming (MIP) problem using PuLP",
        "category": "optimization",
        "module": "handlers.gurddy"
    },
    {
        "name": "solve_production_planning",
        "function": "solve_production_planning",
        "description": "Solve a production planning optimization problem with optional sensitivity analysis",
        "category": "optimization",
        "module": "handlers.gurddy"
    },
    {
        "name": "solve_minimax_game",
        "function": "solve_minimax_game",
        "description": "Solve a two-player zero-sum game using minimax (game theory)",
        "category": "game_theory",
        "module": "handlers.gurddy"
    },
    {
        "name": "solve_minimax_decision",
        "function": "solve_minimax_decision",
        "description": "Solve a minimax decision problem under uncertainty (robust optimization)",
        "category": "game_theory",
        "module": "handlers.gurddy"
    },
    {
        "name": "solve_24_point_game",
        "function": "solve_24_point_game",
        "description": "Solve 24-point game with four numbers using arithmetic operations",
        "category": "classic",
        "module": "handlers.gurddy"
    },
    {
        "name": "solve_chicken_rabbit_problem",
        "function": "solve_chicken_rabbit_problem",
        "description": "Solve classic chicken-rabbit problem with heads and legs constraints",
        "category": "classic",
        "module": "handlers.gurddy"
    },
    {
        "name": "solve_scipy_portfolio_optimization",
        "function": "solve_scipy_portfolio_optimization",
        "description": "Solve nonlinear portfolio optimization using SciPy",
        "category": "scipy",
        "module": "handlers.gurddy"
    },
    {
        "name": "solve_scipy_statistical_fitting",
        "function": "solve_scipy_statistical_fitting",
        "description": "Solve statistical parameter estimation using SciPy",
        "category": "scipy",
        "module": "handlers.gurddy"
    },
    {
        "name": "solve_scipy_facility_location",
        "function": "solve_scipy_facility_location",
        "description": "Solve facility location problem using hybrid CSP-SciPy approach",
        "category": "scipy",
        "module": "handlers.gurddy"
    },
]