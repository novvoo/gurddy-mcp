#!/usr/bin/env python3
"""
Example client for MCP Streamable HTTP transport.

This demonstrates how to use the streamable HTTP endpoint to communicate
with the MCP server using streaming responses.
"""

import requests
import json
from typing import Iterator, Dict, Any


class StreamableMCPClient:
    """Client for MCP server using streamable HTTP transport."""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8080"):
        """Initialize the client.
        
        Args:
            base_url: Base URL of the MCP server
        """
        self.base_url = base_url
        self.http_url = f"{base_url}/mcp/http"
        self.request_id = 0
    
    def _next_id(self) -> int:
        """Get next request ID."""
        self.request_id += 1
        return self.request_id
    
    def call_regular(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make a regular (non-streaming) MCP request.
        
        Args:
            method: MCP method name
            params: Method parameters
            
        Returns:
            Response dictionary
        """
        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": method,
            "params": params or {}
        }
        
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.http_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def call_streaming(self, method: str, params: Dict[str, Any] = None, 
                      use_accept_header: bool = True) -> Iterator[Dict[str, Any]]:
        """Make a streaming MCP request.
        
        Args:
            method: MCP method name
            params: Method parameters
            use_accept_header: If True, use Accept header; otherwise use X-Stream header
            
        Yields:
            Response dictionaries as they arrive
        """
        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": method,
            "params": params or {}
        }
        
        headers = {"Content-Type": "application/json"}
        if use_accept_header:
            headers["Accept"] = "text/event-stream"
        else:
            headers["X-Stream"] = "true"
        
        response = requests.post(self.http_url, headers=headers, json=payload, stream=True)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data: "):
                    data = json.loads(decoded_line[6:])
                    yield data
    
    def list_tools(self, streaming: bool = False) -> Any:
        """List available tools.
        
        Args:
            streaming: If True, use streaming response
            
        Returns:
            Tools list (dict for regular, iterator for streaming)
        """
        if streaming:
            return self.call_streaming("tools/list")
        else:
            return self.call_regular("tools/list")
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None, 
                  streaming: bool = False) -> Any:
        """Call a tool.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments
            streaming: If True, use streaming response
            
        Returns:
            Tool result (dict for regular, iterator for streaming)
        """
        params = {
            "name": tool_name,
            "arguments": arguments or {}
        }
        
        if streaming:
            return self.call_streaming("tools/call", params)
        else:
            return self.call_regular("tools/call", params)


def main():
    """Example usage of the streamable MCP client."""
    print("=" * 70)
    print("MCP Streamable HTTP Client Example")
    print("=" * 70)
    print()
    
    # Create client
    client = StreamableMCPClient()
    
    # Example 1: Regular (non-streaming) request
    print("1. Regular Request - List Tools")
    print("-" * 70)
    try:
        result = client.list_tools(streaming=False)
        print(f"Response: {json.dumps(result, indent=2)}")
        print()
    except Exception as e:
        print(f"Error: {e}\n")
    
    # Example 2: Streaming request with Accept header
    print("2. Streaming Request (Accept header) - Get Info")
    print("-" * 70)
    try:
        for response in client.call_tool("info", streaming=True):
            print(f"Received: {json.dumps(response, indent=2)}")
        print()
    except Exception as e:
        print(f"Error: {e}\n")
    
    # Example 3: Streaming request with X-Stream header
    print("3. Streaming Request (X-Stream header) - Solve 4-Queens")
    print("-" * 70)
    try:
        for response in client.call_streaming("tools/call", {
            "name": "solve_n_queens",
            "arguments": {"n": 4}
        }, use_accept_header=False):
            print(f"Received: {json.dumps(response, indent=2)}")
        print()
    except Exception as e:
        print(f"Error: {e}\n")
    
    # Example 4: Regular request - Solve Sudoku
    print("4. Regular Request - Solve Mini Sudoku")
    print("-" * 70)
    try:
        puzzle = [
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
        result = client.call_tool("solve_sudoku", {"puzzle": puzzle}, streaming=False)
        print(f"Response: {json.dumps(result, indent=2)}")
        print()
    except Exception as e:
        print(f"Error: {e}\n")
    
    # Example 5: Streaming request - Solve 24-point game
    print("5. Streaming Request - Solve 24-Point Game")
    print("-" * 70)
    try:
        for response in client.call_tool("solve_24_point_game", 
                                        {"numbers": [3, 3, 8, 8]}, 
                                        streaming=True):
            print(f"Received: {json.dumps(response, indent=2)}")
        print()
    except Exception as e:
        print(f"Error: {e}\n")
    
    print("=" * 70)
    print("Examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to MCP server")
        print("Please start the server first:")
        print("  uvicorn mcp_server.mcp_http_server:app --host 127.0.0.1 --port 8080")
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
