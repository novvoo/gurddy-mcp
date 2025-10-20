#!/usr/bin/env python3
"""MCP stdio server wrapper for gurddy-mcp.

This server implements the Model Context Protocol (MCP) over stdio,
allowing it to be used as an MCP server in tools like Kiro.
"""
from __future__ import annotations

import asyncio
import json
import sys
from typing import Any

from mcp_server.handlers.gurddy import (
    info as gurddy_info,
    pip_install,
    run_example as run_example_fn,
    solve_sudoku,
    solve_lp,
    solve_csp_generic,
    solve_n_queens,
    solve_graph_coloring,
    solve_map_coloring,
    solve_production_planning,
    solve_minimax_game,
    solve_minimax_decision,
    solve_24_point_game,
    solve_chicken_rabbit_problem,
    solve_scipy_portfolio_optimization,
    solve_scipy_statistical_fitting,
    solve_scipy_facility_location,
)


class MCPStdioServer:
    """MCP stdio server implementation."""
    
    def __init__(self):
        self.tools = {
            "info": {
                "description": "Get information about the gurddy package",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            "install": {
                "description": "Install or upgrade the gurddy package",
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
            "run_example": {
                "description": "Run a gurddy example (lp, csp, n_queens, graph_coloring, map_coloring, scheduling, logic_puzzles, optimized_csp, optimized_lp, minimax, scipy_optimization, classic_problems)",
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
            "solve_n_queens": {
                "description": "Solve the N-Queens problem",
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
            "solve_sudoku": {
                "description": "Solve a 9x9 Sudoku puzzle",
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
            "solve_graph_coloring": {
                "description": "Solve graph coloring problem",
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
            "solve_map_coloring": {
                "description": "Solve map coloring problem",
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
            "solve_lp": {
                "description": "Solve a Linear Programming (LP) or Mixed Integer Programming (MIP) problem using PuLP",
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
            "solve_production_planning": {
                "description": "Solve a production planning optimization problem with optional sensitivity analysis",
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
            "solve_minimax_game": {
                "description": "Solve a two-player zero-sum game using minimax (game theory)",
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
            "solve_minimax_decision": {
                "description": "Solve a minimax decision problem under uncertainty (robust optimization)",
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
            "solve_24_point_game": {
                "description": "Solve 24-point game with four numbers using arithmetic operations",
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
            "solve_chicken_rabbit_problem": {
                "description": "Solve classic chicken-rabbit problem with heads and legs constraints",
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
            "solve_scipy_portfolio_optimization": {
                "description": "Solve nonlinear portfolio optimization using SciPy",
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
            "solve_scipy_statistical_fitting": {
                "description": "Solve statistical parameter estimation using SciPy",
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
            "solve_scipy_facility_location": {
                "description": "Solve facility location problem using hybrid CSP-SciPy approach",
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
            }
        }
    
    async def handle_request(self, request: dict) -> dict:
        """Handle an MCP request."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "gurddy-mcp",
                            "version": "0.1.8"
                        }
                    }
                }
            
            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": [
                            {"name": name, **schema}
                            for name, schema in self.tools.items()
                        ]
                    }
                }
            
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                result = await self.call_tool(tool_name, arguments)
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2, ensure_ascii=False)
                            }
                        ]
                    }
                }
            
            elif method == "notifications/initialized":
                # No response needed for notifications
                return {"jsonrpc": "2.0", "id": request_id, "result": None}
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
        
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    async def call_tool(self, tool_name: str, arguments: dict) -> Any:
        """Call a tool and return the result."""
        if tool_name == "info":
            return gurddy_info()
        
        elif tool_name == "install":
            package = arguments.get("package", "gurddy")
            upgrade = arguments.get("upgrade", False)
            return pip_install(package, upgrade)
        
        elif tool_name == "run_example":
            example = arguments.get("example")
            if not example:
                return {"error": "example parameter is required"}
            return run_example_fn(example)
        
        elif tool_name == "solve_n_queens":
            n = arguments.get("n", 8)
            return solve_n_queens(n)
        
        elif tool_name == "solve_sudoku":
            puzzle = arguments.get("puzzle")
            if not puzzle:
                return {"error": "puzzle parameter is required"}
            return solve_sudoku(puzzle)
        
        elif tool_name == "solve_graph_coloring":
            edges = arguments.get("edges")
            num_vertices = arguments.get("num_vertices")
            max_colors = arguments.get("max_colors", 4)
            if edges is None or num_vertices is None:
                return {"error": "edges and num_vertices are required"}
            return solve_graph_coloring(edges, num_vertices, max_colors)
        
        elif tool_name == "solve_map_coloring":
            regions = arguments.get("regions")
            adjacencies = arguments.get("adjacencies")
            max_colors = arguments.get("max_colors", 4)
            if regions is None or adjacencies is None:
                return {"error": "regions and adjacencies are required"}
            return solve_map_coloring(regions, adjacencies, max_colors)
        
        elif tool_name == "solve_lp":
            profits = arguments.get("profits")
            consumption = arguments.get("consumption")
            capacities = arguments.get("capacities")
            integer = arguments.get("integer", True)
            if profits is None or consumption is None or capacities is None:
                return {"error": "profits, consumption, and capacities are required"}
            problem = {
                "profits": profits,
                "consumption": consumption,
                "capacities": capacities,
                "integer": integer
            }
            return solve_lp(problem)
        
        elif tool_name == "solve_production_planning":
            profits = arguments.get("profits")
            consumption = arguments.get("consumption")
            capacities = arguments.get("capacities")
            integer = arguments.get("integer", True)
            sensitivity_analysis = arguments.get("sensitivity_analysis", False)
            if profits is None or consumption is None or capacities is None:
                return {"error": "profits, consumption, and capacities are required"}
            return solve_production_planning(profits, consumption, capacities, integer, sensitivity_analysis)
        
        elif tool_name == "solve_minimax_game":
            payoff_matrix = arguments.get("payoff_matrix")
            player = arguments.get("player", "row")
            if payoff_matrix is None:
                return {"error": "payoff_matrix is required"}
            return solve_minimax_game(payoff_matrix, player)
        
        elif tool_name == "solve_minimax_decision":
            scenarios = arguments.get("scenarios")
            decision_vars = arguments.get("decision_vars")
            budget = arguments.get("budget", 100.0)
            objective = arguments.get("objective", "minimize_max_loss")
            if scenarios is None or decision_vars is None:
                return {"error": "scenarios and decision_vars are required"}
            return solve_minimax_decision(scenarios, decision_vars, budget, objective)
        
        elif tool_name == "solve_24_point_game":
            numbers = arguments.get("numbers")
            if numbers is None:
                return {"error": "numbers parameter is required"}
            return solve_24_point_game(numbers)
        
        elif tool_name == "solve_chicken_rabbit_problem":
            total_heads = arguments.get("total_heads")
            total_legs = arguments.get("total_legs")
            if total_heads is None or total_legs is None:
                return {"error": "total_heads and total_legs are required"}
            return solve_chicken_rabbit_problem(total_heads, total_legs)
        
        elif tool_name == "solve_scipy_portfolio_optimization":
            expected_returns = arguments.get("expected_returns")
            covariance_matrix = arguments.get("covariance_matrix")
            risk_tolerance = arguments.get("risk_tolerance", 1.0)
            if expected_returns is None or covariance_matrix is None:
                return {"error": "expected_returns and covariance_matrix are required"}
            return solve_scipy_portfolio_optimization(expected_returns, covariance_matrix, risk_tolerance)
        
        elif tool_name == "solve_scipy_statistical_fitting":
            data = arguments.get("data")
            distribution = arguments.get("distribution", "normal")
            if data is None:
                return {"error": "data parameter is required"}
            return solve_scipy_statistical_fitting(data, distribution)
        
        elif tool_name == "solve_scipy_facility_location":
            customer_locations = arguments.get("customer_locations")
            customer_demands = arguments.get("customer_demands")
            facility_locations = arguments.get("facility_locations")
            max_facilities = arguments.get("max_facilities", 2)
            fixed_cost = arguments.get("fixed_cost", 100.0)
            if customer_locations is None or customer_demands is None or facility_locations is None:
                return {"error": "customer_locations, customer_demands, and facility_locations are required"}
            return solve_scipy_facility_location(customer_locations, customer_demands, facility_locations, max_facilities, fixed_cost)
        
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    
    async def run(self):
        """Run the MCP server on stdio."""
        # Read from stdin line by line
        loop = asyncio.get_event_loop()
        
        while True:
            try:
                # Read a line from stdin
                line = await loop.run_in_executor(None, sys.stdin.readline)
                
                if not line:
                    # EOF reached
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                # Parse JSON-RPC request
                try:
                    request = json.loads(line)
                except json.JSONDecodeError as e:
                    # Send error response
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32700,
                            "message": f"Parse error: {str(e)}"
                        }
                    }
                    print(json.dumps(error_response), flush=True)
                    continue
                
                # Handle the request
                response = await self.handle_request(request)
                
                # Send response (if not None, as notifications don't need responses)
                if response is not None:
                    print(json.dumps(response), flush=True)
            
            except Exception as e:
                # Log error to stderr
                print(f"Error in main loop: {e}", file=sys.stderr, flush=True)
                break


def main():
    """Main entry point."""
    server = MCPStdioServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()