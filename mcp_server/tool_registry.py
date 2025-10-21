"""
Central registry for all MCP tools and their metadata.
This is the single source of truth for tool definitions.
"""

from typing import List, Dict, Any

# Tool definitions - single source of truth
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
                    "description": "Package name to install",
                    "default": "gurddy"
                },
                "upgrade": {
                    "type": "boolean",
                    "description": "Whether to upgrade if already installed",
                    "default": False
                }
            },
            "required": []
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
                "example": {
                    "type": "string",
                    "description": "Example name to run",
                    "enum": ["lp", "csp", "n_queens", "graph_coloring", "map_coloring", "scheduling", "logic_puzzles", "optimized_csp", "optimized_lp", "minimax", "scipy_optimization", "classic_problems"]
                }
            },
            "required": ["example"]
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
                    "description": "Board size (number of queens)",
                    "default": 8
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
                    "description": "9x9 grid with 0 for empty cells",
                    "items": {
                        "type": "array",
                        "items": {"type": "integer"}
                    }
                }
            },
            "required": ["puzzle"]
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
                    "description": "List of edges as [vertex1, vertex2] pairs"
                },
                "num_vertices": {
                    "type": "integer",
                    "description": "Number of vertices"
                },
                "max_colors": {
                    "type": "integer",
                    "description": "Maximum number of colors",
                    "default": 4
                }
            },
            "required": ["edges", "num_vertices"]
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
                    "description": "List of region names"
                },
                "adjacencies": {
                    "type": "array",
                    "description": "List of adjacent region pairs"
                },
                "max_colors": {
                    "type": "integer",
                    "description": "Maximum number of colors",
                    "default": 4
                }
            },
            "required": ["regions", "adjacencies"]
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
                "profits": {
                    "type": "object",
                    "description": "Dictionary mapping product names to profit coefficients (objective function)"
                },
                "consumption": {
                    "type": "object",
                    "description": "Dictionary mapping product names to resource consumption (dict of resource->amount)"
                },
                "capacities": {
                    "type": "object",
                    "description": "Dictionary mapping resource names to capacity limits"
                },
                "integer": {
                    "type": "boolean",
                    "description": "Whether to use integer variables (MIP) or continuous (LP)",
                    "default": True
                }
            },
            "required": ["profits", "consumption", "capacities"]
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
                    "description": "Dictionary mapping product names to profit per unit"
                },
                "consumption": {
                    "type": "object",
                    "description": "Dictionary mapping product names to resource consumption"
                },
                "capacities": {
                    "type": "object",
                    "description": "Dictionary mapping resource names to available capacity"
                },
                "integer": {
                    "type": "boolean",
                    "description": "Whether production quantities must be integers",
                    "default": True
                },
                "sensitivity_analysis": {
                    "type": "boolean",
                    "description": "Whether to perform sensitivity analysis",
                    "default": False
                }
            },
            "required": ["profits", "consumption", "capacities"]
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
                    "description": "2D array representing payoffs from row player's perspective",
                    "items": {
                        "type": "array",
                        "items": {"type": "number"}
                    }
                },
                "player": {
                    "type": "string",
                    "description": "Which player's strategy to solve for: 'row' (maximizer) or 'col' (minimizer)",
                    "enum": ["row", "col"],
                    "default": "row"
                }
            },
            "required": ["payoff_matrix"]
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
                    "description": "List of scenarios, each mapping decision variables to loss/gain coefficients",
                    "items": {"type": "object"}
                },
                "decision_vars": {
                    "type": "array",
                    "description": "List of decision variable names",
                    "items": {"type": "string"}
                },
                "budget": {
                    "type": "number",
                    "description": "Total budget constraint",
                    "default": 100.0
                },
                "objective": {
                    "type": "string",
                    "description": "Optimization objective",
                    "enum": ["minimize_max_loss", "maximize_min_gain"],
                    "default": "minimize_max_loss"
                }
            },
            "required": ["scenarios", "decision_vars"]
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
                    "description": "List of exactly 4 integers",
                    "items": {"type": "integer"},
                    "minItems": 4,
                    "maxItems": 4
                }
            },
            "required": ["numbers"]
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
                    "description": "Total number of heads"
                },
                "total_legs": {
                    "type": "integer",
                    "description": "Total number of legs"
                }
            },
            "required": ["total_heads", "total_legs"]
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
                    "description": "Expected returns for each asset",
                    "items": {"type": "number"}
                },
                "covariance_matrix": {
                    "type": "array",
                    "description": "Covariance matrix (2D array)",
                    "items": {
                        "type": "array",
                        "items": {"type": "number"}
                    }
                },
                "risk_tolerance": {
                    "type": "number",
                    "description": "Risk tolerance parameter",
                    "default": 1.0
                }
            },
            "required": ["expected_returns", "covariance_matrix"]
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
                    "description": "List of data points",
                    "items": {"type": "number"}
                },
                "distribution": {
                    "type": "string",
                    "description": "Distribution type to fit",
                    "enum": ["normal", "exponential", "uniform"],
                    "default": "normal"
                }
            },
            "required": ["data"]
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
                    "description": "List of [x, y] coordinates for customers",
                    "items": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 2,
                        "maxItems": 2
                    }
                },
                "customer_demands": {
                    "type": "array",
                    "description": "List of demand values for each customer",
                    "items": {"type": "number"}
                },
                "facility_locations": {
                    "type": "array",
                    "description": "List of [x, y] coordinates for potential facilities",
                    "items": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 2,
                        "maxItems": 2
                    }
                },
                "max_facilities": {
                    "type": "integer",
                    "description": "Maximum number of facilities to select",
                    "default": 2
                },
                "fixed_cost": {
                    "type": "number",
                    "description": "Fixed cost for opening each facility",
                    "default": 100.0
                }
            },
            "required": ["customer_locations", "customer_demands", "facility_locations"]
        }
    },
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
