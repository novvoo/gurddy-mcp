"""Register all gurddy tools using central registry."""
from mcp_server.core import tool
from mcp_server.tool_registry import TOOLS
from mcp_server.handlers import gurddy


# Dynamically register all tools from central registry
for tool_def in TOOLS:
    tool_name = tool_def["name"]
    func_name = tool_def["function"]
    description = tool_def["description"]
    input_schema = tool_def["inputSchema"]
    
    # Get the handler function
    handler_func = getattr(gurddy, func_name)
    
    # Create wrapper function with proper name
    def create_wrapper(handler, name):
        """Create a wrapper function for the tool."""
        def wrapper(**kwargs):
            # Handle special case for solve_lp which expects a problem dict
            if name == "solve_lp":
                problem = {
                    "profits": kwargs.get("profits"),
                    "consumption": kwargs.get("consumption"),
                    "capacities": kwargs.get("capacities"),
                    "integer": kwargs.get("integer", True)
                }
                return handler(problem)
            return handler(**kwargs)
        wrapper.__name__ = name
        return wrapper
    
    # Create and register the wrapper
    wrapper_func = create_wrapper(handler_func, tool_name)
    
    # Register with decorator
    tool(name=tool_name, description=description, input_schema=input_schema)(wrapper_func)
