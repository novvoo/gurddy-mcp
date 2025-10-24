"""
Central registry for all MCP tools and their metadata.
This is the single source of truth for tool definitions.

NOTE: Schemas are auto-generated from function signatures.
Run `python scripts/generate_registry.py` to update.
"""

from typing import List, Dict, Any

# Tool definitions - single source of truth
# Schemas auto-generated from function signatures
TOOLS = [
    {
        "name": "info",
        "function": "info",
        "description": "Get information about the gurddy package",
        "category": "meta",
        "module": "handlers.gurddy",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "install",
        "function": "pip_install",
        "description": "Install or upgrade the gurddy package",
        "category": "meta",
        "module": "handlers.gurddy",
        "inputSchema": {
            "type": "object",
            "properties": {
                "package": {
                    "type": "string",
                    "description": "Parameter package"
                },
                "upgrade": {
                    "type": "boolean",
                    "description": "Parameter upgrade"
                }
            },
            "required": [
                "package"
            ]
        }
    },
    {
        "name": "run_example",
        "function": "run_example",
        "description": "Run a gurddy example (lp, csp, n_queens, graph_coloring, map_coloring, scheduling, logic_puzzles, optimized_csp, optimized_lp, minimax, scipy_optimization, classic_problems)",
        "category": "examples",
        "module": "handlers.gurddy",
        "inputSchema": {
            "type": "object",
            "properties": {
                "example_name": {
                    "type": "string",
                    "description": "Parameter example_name"
                }
            },
            "required": [
                "example_name"
            ]
        }
    },
    {
        "name": "solve_n_queens",
        "function": "solve_n_queens",
        "description": "Solve the N-Queens problem",
        "category": "csp",
        "module": "handlers.gurddy",
        "inputSchema": {
            "type": "object",
            "properties": {
                "n": {
                    "type": "integer",
                    "description": "Parameter n"
                }
            },
            "required": []
        }
    },
    {
        "name": "solve_sudoku",
        "function": "solve_sudoku",
        "description": "Solve a 9x9 Sudoku puzzle",
        "category": "csp",
        "module": "handlers.gurddy",
        "inputSchema": {
            "type": "object",
            "properties": {
                "puzzle": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "integer"
                        }
                    },
                    "description": "Parameter puzzle"
                }
            },
            "required": [
                "puzzle"
            ]
        }
    },
    {
        "name": "solve_graph_coloring",
        "function": "solve_graph_coloring",
        "description": "Solve graph coloring problem",
        "category": "csp",
        "module": "handlers.gurddy",
        "inputSchema": {
            "type": "object",
            "properties": {
                "edges": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "integer"
                        }
                    },
                    "description": "Parameter edges"
                },
                "num_vertices": {
                    "type": "integer",
                    "description": "Parameter num_vertices"
                },
                "max_colors": {
                    "type": "integer",
                    "description": "Parameter max_colors"
                }
            },
            "required": [
                "edges",
                "num_vertices"
            ]
        }
    },
    {
        "name": "solve_map_coloring",
        "function": "solve_map_coloring",
        "description": "Solve map coloring problem",
        "category": "csp",
        "module": "handlers.gurddy",
        "inputSchema": {
            "type": "object",
            "properties": {
                "regions": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Parameter regions"
                },
                "adjacencies": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "description": "Parameter adjacencies"
                },
                "max_colors": {
                    "type": "integer",
                    "description": "Parameter max_colors"
                }
            },
            "required": [
                "regions",
                "adjacencies"
            ]
        }
    },
    {
        "name": "solve_lp",
        "function": "solve_lp",
        "description": "Solve a Linear Programming (LP) or Mixed Integer Programming (MIP) problem using PuLP",
        "category": "optimization",
        "module": "handlers.gurddy",
        "inputSchema": {
            "type": "object",
            "properties": {
                "problem": {
                    "type": "object",
                    "description": "Parameter problem"
                }
            },
            "required": [
                "problem"
            ]
        }
    },
    {
        "name": "solve_production_planning",
        "function": "solve_production_planning",
        "description": "Solve a production planning optimization problem with optional sensitivity analysis",
        "category": "optimization",
        "module": "handlers.gurddy",
        "inputSchema": {
            "type": "object",
            "properties": {
                "profits": {
                    "type": "object",
                    "description": "Parameter profits"
                },
                "consumption": {
                    "type": "object",
                    "description": "Parameter consumption"
                },
                "capacities": {
                    "type": "object",
                    "description": "Parameter capacities"
                },
                "integer": {
                    "type": "boolean",
                    "description": "Parameter integer"
                },
                "sensitivity_analysis": {
                    "type": "boolean",
                    "description": "Parameter sensitivity_analysis"
                }
            },
            "required": [
                "profits",
                "consumption",
                "capacities"
            ]
        }
    },
    {
        "name": "solve_minimax_game",
        "function": "solve_minimax_game",
        "description": "Solve a two-player zero-sum game using minimax (game theory)",
        "category": "game_theory",
        "module": "handlers.gurddy",
        "inputSchema": {
            "type": "object",
            "properties": {
                "payoff_matrix": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        }
                    },
                    "description": "Parameter payoff_matrix"
                },
                "player": {
                    "type": "string",
                    "description": "Parameter player"
                }
            },
            "required": [
                "payoff_matrix"
            ]
        }
    },
    {
        "name": "solve_minimax_decision",
        "function": "solve_minimax_decision",
        "description": "Solve a minimax decision problem under uncertainty (robust optimization)",
        "category": "game_theory",
        "module": "handlers.gurddy",
        "inputSchema": {
            "type": "object",
            "properties": {
                "scenarios": {
                    "type": "array",
                    "items": {
                        "type": "object"
                    },
                    "description": "Parameter scenarios"
                },
                "decision_vars": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Parameter decision_vars"
                },
                "budget": {
                    "type": "number",
                    "description": "Parameter budget"
                },
                "objective": {
                    "type": "string",
                    "description": "Parameter objective"
                }
            },
            "required": [
                "scenarios",
                "decision_vars"
            ]
        }
    },
    {
        "name": "solve_24_point_game",
        "function": "solve_24_point_game",
        "description": "Solve 24-point game with four numbers using arithmetic operations",
        "category": "classic",
        "module": "handlers.gurddy",
        "inputSchema": {
            "type": "object",
            "properties": {
                "numbers": {
                    "type": "array",
                    "items": {
                        "type": "integer"
                    },
                    "description": "Parameter numbers"
                }
            },
            "required": [
                "numbers"
            ]
        }
    },
    {
        "name": "solve_chicken_rabbit_problem",
        "function": "solve_chicken_rabbit_problem",
        "description": "Solve classic chicken-rabbit problem with heads and legs constraints",
        "category": "classic",
        "module": "handlers.gurddy",
        "inputSchema": {
            "type": "object",
            "properties": {
                "total_heads": {
                    "type": "integer",
                    "description": "Parameter total_heads"
                },
                "total_legs": {
                    "type": "integer",
                    "description": "Parameter total_legs"
                }
            },
            "required": [
                "total_heads",
                "total_legs"
            ]
        }
    },
    {
        "name": "solve_scipy_portfolio_optimization",
        "function": "solve_scipy_portfolio_optimization",
        "description": "Solve nonlinear portfolio optimization using SciPy",
        "category": "scipy",
        "module": "handlers.gurddy",
        "inputSchema": {
            "type": "object",
            "properties": {
                "expected_returns": {
                    "type": "array",
                    "items": {
                        "type": "number"
                    },
                    "description": "Parameter expected_returns"
                },
                "covariance_matrix": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        }
                    },
                    "description": "Parameter covariance_matrix"
                },
                "risk_tolerance": {
                    "type": "number",
                    "description": "Parameter risk_tolerance"
                }
            },
            "required": [
                "expected_returns",
                "covariance_matrix"
            ]
        }
    },
    {
        "name": "solve_scipy_statistical_fitting",
        "function": "solve_scipy_statistical_fitting",
        "description": "Solve statistical parameter estimation using SciPy",
        "category": "scipy",
        "module": "handlers.gurddy",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {
                        "type": "number"
                    },
                    "description": "Parameter data"
                },
                "distribution": {
                    "type": "string",
                    "description": "Parameter distribution"
                }
            },
            "required": [
                "data"
            ]
        }
    },
    {
        "name": "solve_scipy_facility_location",
        "function": "solve_scipy_facility_location",
        "description": "Solve facility location problem using hybrid CSP-SciPy approach",
        "category": "scipy",
        "module": "handlers.gurddy",
        "inputSchema": {
            "type": "object",
            "properties": {
                "customer_locations": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        }
                    },
                    "description": "Parameter customer_locations"
                },
                "customer_demands": {
                    "type": "array",
                    "items": {
                        "type": "number"
                    },
                    "description": "Parameter customer_demands"
                },
                "facility_locations": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        }
                    },
                    "description": "Parameter facility_locations"
                },
                "max_facilities": {
                    "type": "integer",
                    "description": "Parameter max_facilities"
                },
                "fixed_cost": {
                    "type": "number",
                    "description": "Parameter fixed_cost"
                }
            },
            "required": [
                "customer_locations",
                "customer_demands",
                "facility_locations"
            ]
        }
    }
]


def get_all_tool_names() -> List[str]:
    """Get list of all tool names."""
    return [tool["name"] for tool in TOOLS]


def get_all_function_names() -> List[str]:
    """Get list of all function names for imports."""
    return [tool["function"] for tool in TOOLS]


def get_tools_by_category(category: str) -> List[Dict[str, Any]]:
    """Get tools filtered by category."""
    return [tool for tool in TOOLS if tool["category"] == category]


def get_tool_count() -> int:
    """Get total number of tools."""
    return len(TOOLS)


def get_categories() -> List[str]:
    """Get list of all categories."""
    return list(set(tool["category"] for tool in TOOLS))


def get_tool_schemas() -> Dict[str, Dict[str, Any]]:
    """Get tool schemas for MCP server registration.
    
    Returns:
        Dict mapping tool name to schema (description + inputSchema)
    """
    schemas = {}
    for tool in TOOLS:
        schemas[tool["name"]] = {
            "description": tool["description"],
            "inputSchema": tool["inputSchema"]
        }
    return schemas


def get_tool_by_name(name: str) -> Dict[str, Any]:
    """Get tool definition by name."""
    for tool in TOOLS:
        if tool["name"] == name:
            return tool
    return None


def get_function_name_mapping() -> Dict[str, str]:
    """Get mapping from tool name to function name.
    
    Returns:
        Dict mapping tool name to function name
    """
    return {tool["name"]: tool["function"] for tool in TOOLS}


def generate_tool_list_markdown() -> str:
    """Generate markdown list of all tools for documentation."""
    lines = []
    for tool in TOOLS:
        lines.append(f"- `{tool['name']}` - {tool['description']}")
    return "\n".join(lines)


def generate_auto_approve_list() -> List[str]:
    """Generate list of tool names for MCP auto-approve configuration."""
    return get_all_tool_names()


# Export commonly used values
ALL_TOOL_NAMES = get_all_tool_names()
ALL_FUNCTION_NAMES = get_all_function_names()
TOOL_COUNT = get_tool_count()
TOOL_SCHEMAS = get_tool_schemas()
FUNCTION_NAME_MAPPING = get_function_name_mapping()
