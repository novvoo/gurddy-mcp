"""MCP HTTP server implementation."""
import json
from typing import Dict

from .tool_registry import get_registry


class MCPHTTPServer:
    """MCP HTTP server implementation."""
    
    def __init__(self):
        self.registry = get_registry()
    
    async def handle_request(self, request: Dict) -> Dict:
        """Handle an MCP request."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "initialize":
                return self._handle_initialize(request_id)
            
            elif method == "tools/list":
                return self._handle_tools_list(request_id)
            
            elif method == "tools/call":
                return await self._handle_tools_call(request_id, params)
            
            elif method == "notifications/initialized":
                # No response needed for notifications
                return {}
            
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
    
    def _handle_initialize(self, request_id) -> Dict:
        """Handle initialize request."""
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
    
    def _handle_tools_list(self, request_id) -> Dict:
        """Handle tools/list request."""
        tools = self.registry.get_tools()
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {"name": name, **schema}
                    for name, schema in tools.items()
                ]
            }
        }
    
    async def _handle_tools_call(self, request_id, params: Dict) -> Dict:
        """Handle tools/call request."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        result = await self.registry.call_tool(tool_name, arguments)
        
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
