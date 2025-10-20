#!/usr/bin/env python3
"""Example HTTP MCP client for gurddy-mcp.

This demonstrates how to interact with the HTTP MCP server following MCP protocol requirements.
"""
import json
import requests
import time
from typing import Dict, Any, Optional


class MCPHTTPClient:
    """MCP HTTP client with proper protocol handling."""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8080"):
        self.base_url = base_url
        self.request_id = 0
        self.initialized = False
        self.server_info = None
        self.capabilities = None
    
    def _get_next_id(self) -> int:
        """Get next request ID."""
        self.request_id += 1
        return self.request_id
    
    def _make_request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a JSON-RPC 2.0 request to the MCP server."""
        request = {
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": method
        }
        
        if params is not None:
            request["params"] = params
        
        try:
            response = requests.post(f"{self.base_url}/message", json=request, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "jsonrpc": "2.0",
                "id": request["id"],
                "error": {
                    "code": -32603,
                    "message": f"HTTP request failed: {str(e)}"
                }
            }
    
    def check_connection(self) -> Dict[str, Any]:
        """Check if the server is reachable."""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            response.raise_for_status()
            return {
                "success": True,
                "status": "connected",
                "server_info": response.json()
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "status": "connection_failed",
                "error": str(e)
            }
    
    def initialize(self) -> Dict[str, Any]:
        """Initialize the MCP connection."""
        result = self._make_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "clientInfo": {
                "name": "gurddy-mcp-http-client",
                "version": "0.1.0"
            }
        })
        
        if "result" in result:
            self.initialized = True
            self.server_info = result["result"].get("serverInfo")
            self.capabilities = result["result"].get("capabilities")
            
            # Send initialized notification
            self._make_request("notifications/initialized")
        
        return result
    
    def list_tools(self) -> Dict[str, Any]:
        """List available MCP tools."""
        if not self.initialized:
            return {
                "error": "Client not initialized. Call initialize() first."
            }
        
        return self._make_request("tools/list")
    
    def call_tool(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Call an MCP tool."""
        if not self.initialized:
            return {
                "error": "Client not initialized. Call initialize() first."
            }
        
        if arguments is None:
            arguments = {}
        
        return self._make_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
    
    def get_server_info(self) -> Optional[Dict[str, Any]]:
        """Get server information from initialization."""
        return self.server_info
    
    def get_capabilities(self) -> Optional[Dict[str, Any]]:
        """Get server capabilities from initialization."""
        return self.capabilities


# Legacy functions for backward compatibility
def call_mcp_tool(base_url: str, tool_name: str, arguments: dict | None = None) -> dict:
    """Call an MCP tool via HTTP (legacy function)."""
    client = MCPHTTPClient(base_url)
    client.initialize()
    return client.call_tool(tool_name, arguments)


def list_tools(base_url: str) -> dict:
    """List available MCP tools (legacy function)."""
    client = MCPHTTPClient(base_url)
    client.initialize()
    return client.list_tools()


def demonstrate_basic_usage():
    """Demonstrate basic MCP client usage with proper protocol handling."""
    print("=== Basic MCP Client Usage ===\n")
    
    client = MCPHTTPClient()
    
    # Step 1: Check connection
    print("1. Checking server connection...")
    connection_result = client.check_connection()
    if not connection_result["success"]:
        print(f"❌ Connection failed: {connection_result['error']}")
        return False
    
    print(f"✅ Server connected: {connection_result['server_info']['name']}")
    print()
    
    # Step 2: Initialize MCP connection
    print("2. Initializing MCP connection...")
    init_result = client.initialize()
    
    if "error" in init_result:
        print(f"❌ Initialization failed: {init_result['error']}")
        return False
    
    server_info = client.get_server_info()
    print(f"✅ MCP initialized successfully")
    print(f"   Server: {server_info['name']} v{server_info['version']}")
    print(f"   Protocol: {init_result['result']['protocolVersion']}")
    print()
    
    # Step 3: List available tools
    print("3. Listing available tools...")
    tools_result = client.list_tools()
    
    if "error" in tools_result:
        print(f"❌ Failed to list tools: {tools_result['error']}")
        return False
    
    tools = tools_result.get("result", {}).get("tools", [])
    print(f"✅ Found {len(tools)} tools:")
    for tool in tools[:5]:  # Show first 5 tools
        print(f"   - {tool['name']}: {tool['description'][:60]}...")
    if len(tools) > 5:
        print(f"   ... and {len(tools) - 5} more tools")
    print()
    
    return True


def demonstrate_tool_calls():
    """Demonstrate various tool calls with proper error handling."""
    print("=== Tool Call Examples ===\n")
    
    client = MCPHTTPClient()
    client.initialize()
    
    examples = [
        {
            "name": "Package Information",
            "tool": "info",
            "args": {},
            "description": "Get gurddy package information"
        },
        {
            "name": "N-Queens Problem",
            "tool": "solve_n_queens",
            "args": {"n": 4},
            "description": "Solve 4-Queens problem"
        },
        {
            "name": "Graph Coloring",
            "tool": "solve_graph_coloring",
            "args": {
                "edges": [[0, 1], [1, 2], [2, 0]],
                "num_vertices": 3,
                "max_colors": 3
            },
            "description": "Color a triangle graph"
        },
        {
            "name": "Sudoku Solver",
            "tool": "solve_sudoku",
            "args": {
                "puzzle": [
                    [5, 3, 0, 0, 7, 0, 0, 0, 0],
                    [6, 0, 0, 1, 9, 5, 0, 0, 0],
                    [0, 9, 8, 0, 0, 0, 0, 6, 0],
                    [8, 0, 0, 0, 6, 0, 0, 0, 3],
                    [4, 0, 0, 8, 0, 3, 0, 0, 1],
                    [7, 0, 0, 0, 2, 0, 0, 0, 6],
                    [0, 6, 0, 0, 0, 0, 2, 8, 0],
                    [0, 0, 0, 4, 1, 9, 0, 0, 5],
                    [0, 0, 0, 0, 8, 0, 0, 7, 9]
                ]
            },
            "description": "Solve a Sudoku puzzle"
        },
        {
            "name": "Linear Programming",
            "tool": "solve_lp",
            "args": {
                "profits": {"A": 3, "B": 2},
                "consumption": {
                    "A": {"material": 2, "labor": 1},
                    "B": {"material": 1, "labor": 2}
                },
                "capacities": {"material": 100, "labor": 80}
            },
            "description": "Solve production optimization problem"
        },
        {
            "name": "24-Point Game",
            "tool": "solve_24_point_game",
            "args": {"numbers": [4, 1, 8, 7]},
            "description": "Solve 24-point game with [4,1,8,7]"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['name']}")
        print(f"   Description: {example['description']}")
        
        result = client.call_tool(example["tool"], example["args"])
        
        if "error" in result:
            print(f"   ❌ Error: {result['error']['message']}")
        elif "result" in result:
            content_list = result["result"].get("content", [])
            if not content_list:
                print(f"   ⚠️  Empty content in response")
                continue
            
            content = content_list[0].get("text", "")
            if not content:
                print(f"   ⚠️  Empty text content")
                continue
            
            try:
                solution = json.loads(content)
                
                # Handle different response formats
                if isinstance(solution, dict):
                    if solution.get("success"):
                        if "solution" in solution:
                            sol_str = str(solution["solution"])
                            if len(sol_str) > 100:
                                sol_str = sol_str[:100] + "..."
                            print(f"   ✅ Solution: {sol_str}")
                        elif "name" in solution and "version" in solution:
                            # Package info response
                            print(f"   ✅ Package: {solution['name']} v{solution['version']}")
                        else:
                            print(f"   ✅ Success: {solution.get('message', 'Completed')}")
                    elif solution.get("success") is False:
                        print(f"   ❌ Failed: {solution.get('error', 'Unknown error')}")
                    else:
                        # Response without explicit success field (like package info)
                        if "name" in solution:
                            print(f"   ✅ Package: {solution['name']} v{solution.get('version', 'unknown')}")
                        else:
                            print(f"   ✅ Result: {str(solution)[:100]}...")
                else:
                    print(f"   ✅ Result: {str(solution)[:100]}...")
                    
            except json.JSONDecodeError as e:
                print(f"   ⚠️  JSON decode error: {e}")
                print(f"   Raw content: {content[:100]}...")
        else:
            print(f"   ⚠️  Unexpected response format: {result}")
        
        print()


def demonstrate_error_handling():
    """Demonstrate error handling scenarios."""
    print("=== Error Handling Examples ===\n")
    
    client = MCPHTTPClient()
    client.initialize()
    
    error_cases = [
        {
            "name": "Invalid Tool Name",
            "tool": "nonexistent_tool",
            "args": {},
            "expected": "Tool not found error"
        },
        {
            "name": "Missing Required Parameters",
            "tool": "solve_graph_coloring",
            "args": {"edges": [[0, 1]]},  # Missing num_vertices
            "expected": "Missing parameter error"
        },
        {
            "name": "Invalid Parameter Type",
            "tool": "solve_n_queens",
            "args": {"n": "invalid"},  # Should be integer
            "expected": "Type error"
        }
    ]
    
    for i, case in enumerate(error_cases, 1):
        print(f"{i}. {case['name']}")
        print(f"   Expected: {case['expected']}")
        
        result = client.call_tool(case["tool"], case["args"])
        
        if "error" in result:
            print(f"   ✅ Error handled: {result['error']['message']}")
        elif "result" in result:
            content = result["result"].get("content", [{}])[0].get("text", "")
            try:
                solution = json.loads(content)
                if not solution.get("success"):
                    print(f"   ✅ Tool error: {solution.get('error', 'Unknown error')}")
                else:
                    print(f"   ⚠️  Unexpected success")
            except json.JSONDecodeError:
                print(f"   ⚠️  Unexpected response: {content[:50]}...")
        
        print()


def demonstrate_advanced_examples():
    """Demonstrate advanced optimization problems."""
    print("=== Advanced Optimization Examples ===\n")
    
    client = MCPHTTPClient()
    client.initialize()
    
    advanced_examples = [
        {
            "name": "Portfolio Optimization",
            "tool": "solve_scipy_portfolio_optimization",
            "args": {
                "expected_returns": [0.12, 0.18, 0.15],
                "covariance_matrix": [
                    [0.04, 0.01, 0.02],
                    [0.01, 0.09, 0.03],
                    [0.02, 0.03, 0.06]
                ],
                "risk_tolerance": 0.5
            },
            "description": "Optimize investment portfolio"
        },
        {
            "name": "Facility Location",
            "tool": "solve_scipy_facility_location",
            "args": {
                "customer_locations": [[0, 0], [10, 0], [5, 10]],
                "customer_demands": [100, 150, 80],
                "facility_locations": [[2, 2], [8, 3], [6, 8]],
                "max_facilities": 2,
                "fixed_cost": 50.0
            },
            "description": "Find optimal facility locations"
        },
        {
            "name": "Minimax Game Theory",
            "tool": "solve_minimax_game",
            "args": {
                "payoff_matrix": [
                    [3, -1, 4],
                    [1, 5, -2],
                    [2, 1, 3]
                ],
                "player": "row"
            },
            "description": "Solve zero-sum game"
        },
        {
            "name": "Production Planning",
            "tool": "solve_production_planning",
            "args": {
                "profits": {"ProductA": 40, "ProductB": 30},
                "consumption": {
                    "ProductA": {"Material1": 2, "Material2": 1, "Labor": 3},
                    "ProductB": {"Material1": 1, "Material2": 2, "Labor": 2}
                },
                "capacities": {"Material1": 100, "Material2": 80, "Labor": 120},
                "integer": True,
                "sensitivity_analysis": True
            },
            "description": "Optimize production with sensitivity analysis"
        }
    ]
    
    for i, example in enumerate(advanced_examples, 1):
        print(f"{i}. {example['name']}")
        print(f"   Description: {example['description']}")
        
        result = client.call_tool(example["tool"], example["args"])
        
        if "error" in result:
            print(f"   ❌ Error: {result['error']['message']}")
        elif "result" in result:
            content = result["result"].get("content", [{}])[0].get("text", "")
            try:
                solution = json.loads(content)
                if solution.get("success"):
                    print(f"   ✅ Optimization completed successfully")
                    if "objective_value" in solution:
                        print(f"      Objective value: {solution['objective_value']}")
                    if "solution" in solution and isinstance(solution["solution"], dict):
                        print(f"      Variables: {len(solution['solution'])} optimized")
                else:
                    print(f"   ❌ Failed: {solution.get('error', 'Unknown error')}")
            except json.JSONDecodeError:
                print(f"   ⚠️  Response: {content[:80]}...")
        
        print()


def main():
    """Main example demonstrating comprehensive MCP client usage."""
    print("=== Gurddy HTTP MCP Client - Comprehensive Examples ===\n")
    
    # Basic usage demonstration
    if not demonstrate_basic_usage():
        return
    
    # Tool call examples
    demonstrate_tool_calls()
    
    # Error handling
    demonstrate_error_handling()
    
    # Advanced examples
    demonstrate_advanced_examples()
    
    print("🎉 All examples completed successfully!")
    print("\nFor more information:")
    print("- Server documentation: http://127.0.0.1:8080/docs")
    print("- MCP Protocol: https://modelcontextprotocol.io/")


def quick_example():
    """Quick example for testing basic functionality."""
    print("=== Quick Test ===\n")
    
    client = MCPHTTPClient()
    
    # Check connection
    print("1. Checking connection...")
    conn = client.check_connection()
    if not conn["success"]:
        print(f"❌ Cannot connect: {conn['error']}")
        return
    print(f"✅ Server reachable: {conn['server_info']['name']}")
    
    # Initialize
    print("\n2. Initializing MCP...")
    init_result = client.initialize()
    if "error" in init_result:
        print(f"❌ Initialization failed: {init_result['error']}")
        return
    print("✅ MCP initialized")
    
    # Test info tool
    print("\n3. Testing info tool...")
    result = client.call_tool("info")
    
    if "error" in result:
        print(f"❌ Tool call failed: {result['error']['message']}")
    elif "result" in result:
        content_list = result["result"].get("content", [])
        if content_list:
            content = content_list[0].get("text", "")
            try:
                info = json.loads(content)
                if "name" in info:
                    print(f"✅ Connected to {info['name']} v{info.get('version', 'unknown')}")
                else:
                    print(f"✅ Response: {str(info)[:100]}...")
            except json.JSONDecodeError:
                print(f"✅ Raw response: {content[:100]}...")
        else:
            print("❌ Empty response content")
    else:
        print(f"❌ Unexpected response: {result}")
    
    print("\n🎉 Quick test completed!")


if __name__ == "__main__":
    import sys
    
    # Note: Make sure the HTTP MCP server is running:
    # uvicorn mcp_server.mcp_http_server:app --host 127.0.0.1 --port 8080
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_example()
    else:
        try:
            main()
        except requests.exceptions.ConnectionError:
            print("❌ Error: Could not connect to HTTP MCP server.")
            print("\nTo start the server, run:")
            print("  uvicorn mcp_server.mcp_http_server:app --host 127.0.0.1 --port 8080")
            print("\nOr for quick testing:")
            print("  python examples/http_mcp_client.py quick")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("Please check that the MCP server is running and accessible.")
