"""Tool registry for MCP server."""
from typing import Any, Callable, Dict, Optional
import inspect


class ToolRegistry:
    """Registry for MCP tools with decorator-based registration."""
    
    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._handlers: Dict[str, Callable] = {}
    
    def register(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        handler: Callable
    ):
        """Register a tool with its schema and handler."""
        self._tools[name] = {
            "description": description,
            "inputSchema": input_schema
        }
        self._handlers[name] = handler
    
    def get_tools(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered tools."""
        return self._tools
    
    def get_handler(self, name: str) -> Optional[Callable]:
        """Get handler for a tool."""
        return self._handlers.get(name)
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Call a tool by name with arguments."""
        handler = self.get_handler(name)
        if not handler:
            return {"error": f"Unknown tool: {name}"}
        
        try:
            # Check if handler is async
            if inspect.iscoroutinefunction(handler):
                return await handler(**arguments)
            else:
                return handler(**arguments)
        except TypeError as e:
            return {"error": f"Invalid arguments: {str(e)}"}
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}


# Global registry instance
_registry = ToolRegistry()


def tool(name: str, description: str, input_schema: Dict[str, Any]):
    """Decorator to register a tool."""
    def decorator(func: Callable):
        _registry.register(name, description, input_schema, func)
        return func
    return decorator


def get_registry() -> ToolRegistry:
    """Get the global tool registry."""
    return _registry
