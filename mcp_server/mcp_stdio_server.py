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
import inspect

from mcp_server.tool_registry import TOOL_SCHEMAS, get_tool_by_name
from mcp_server.handlers import gurddy


class MCPStdioServer:
    """MCP stdio server implementation."""
    
    def __init__(self):
        # Use tool schemas from central registry
        self.tools = TOOL_SCHEMAS
        
        # Build function mapping from registry
        self.function_map = {}
        for tool_name in self.tools.keys():
            tool_def = get_tool_by_name(tool_name)
            if tool_def:
                func_name = tool_def["function"]
                # Get the actual function from gurddy handlers module
                if hasattr(gurddy, func_name):
                    self.function_map[tool_name] = getattr(gurddy, func_name)
                else:
                    raise AttributeError(f"Function {func_name} not found in gurddy handlers")
    
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
                return None
            
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
        if tool_name not in self.function_map:
            return {"error": f"Unknown tool: {tool_name}"}
        
        func = self.function_map[tool_name]
        
        try:
            # Handle special cases that need argument transformation
            if tool_name == "solve_lp":
                # solve_lp expects a problem dict
                problem = {
                    "profits": arguments.get("profits"),
                    "consumption": arguments.get("consumption"),
                    "capacities": arguments.get("capacities"),
                    "integer": arguments.get("integer", True)
                }
                return func(problem)
            
            # For all other tools, pass arguments directly
            # Get function signature to handle defaults properly
            sig = inspect.signature(func)
            call_args = {}
            
            for param_name, param in sig.parameters.items():
                if param_name in arguments:
                    call_args[param_name] = arguments[param_name]
                elif param.default != inspect.Parameter.empty:
                    # Use default value from function signature
                    call_args[param_name] = param.default
            
            return func(**call_args)
            
        except TypeError as e:
            return {"error": f"Invalid arguments: {str(e)}"}
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}
    
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
