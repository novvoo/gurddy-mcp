#!/usr/bin/env python3
"""Example HTTP MCP client for gurddy-mcp.

This demonstrates how to interact with the HTTP MCP server.
"""
import json
import requests


def call_mcp_tool(base_url: str, tool_name: str, arguments: dict = None) -> dict:
    """Call an MCP tool via HTTP."""
    if arguments is None:
        arguments = {}
    
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    response = requests.post(f"{base_url}/message", json=request)
    return response.json()


def list_tools(base_url: str) -> dict:
    """List available MCP tools."""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {}
    }
    
    response = requests.post(f"{base_url}/message", json=request)
    return response.json()


def main():
    """Main example."""
    base_url = "http://127.0.0.1:8080"
    
    print("=== Gurddy HTTP MCP Client Example ===\n")
    
    # Example 1: List available tools
    print("1. Listing available tools...")
    result = list_tools(base_url)
    tools = result.get("result", {}).get("tools", [])
    print(f"Found {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool['name']}: {tool['description']}")
    print()
    
    # Example 2: Get package info
    print("2. Getting package info...")
    result = call_mcp_tool(base_url, "info")
    content = result.get("result", {}).get("content", [{}])[0].get("text", "")
    info = json.loads(content)
    print(f"Package: {info['name']}")
    print(f"Description: {info['description'][:100]}...")
    print()
    
    # Example 3: Solve N-Queens problem
    print("3. Solving 4-Queens problem...")
    result = call_mcp_tool(base_url, "solve_n_queens", {"n": 4})
    content = result.get("result", {}).get("content", [{}])[0].get("text", "")
    solution = json.loads(content)
    if solution.get("success"):
        print(f"Solution found: {solution.get('solution')}")
    else:
        print(f"Error: {solution.get('error')}")
    print()
    
    # Example 4: Solve graph coloring
    print("4. Solving graph coloring problem...")
    result = call_mcp_tool(base_url, "solve_graph_coloring", {
        "edges": [[0, 1], [1, 2], [2, 0]],
        "num_vertices": 3,
        "max_colors": 3
    })
    content = result.get("result", {}).get("content", [{}])[0].get("text", "")
    solution = json.loads(content)
    if solution.get("success"):
        print(f"Solution found: {solution.get('solution')}")
    else:
        print(f"Error: {solution.get('error')}")
    print()
    
    print("✅ All examples completed!")


if __name__ == "__main__":
    # Note: Make sure the HTTP MCP server is running:
    # uvicorn mcp_server.mcp_http_server:app --host 127.0.0.1 --port 8080
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to HTTP MCP server.")
        print("Please start the server first:")
        print("  uvicorn mcp_server.mcp_http_server:app --host 127.0.0.1 --port 8080")
