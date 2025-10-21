"""Test consistency between tool_registry and mcp_stdio_server."""
import pytest
from mcp_server.tool_registry import TOOLS, TOOL_SCHEMAS, get_tool_by_name
from mcp_server.mcp_stdio_server import MCPStdioServer
from mcp_server.handlers import gurddy


def test_all_tools_have_schemas():
    """Test that all tools have complete schemas."""
    for tool in TOOLS:
        assert "name" in tool
        assert "function" in tool
        assert "description" in tool
        assert "category" in tool
        assert "module" in tool
        assert "inputSchema" in tool
        assert "type" in tool["inputSchema"]
        assert "properties" in tool["inputSchema"]
        assert "required" in tool["inputSchema"]


def test_all_functions_exist():
    """Test that all registered functions exist in handlers."""
    for tool in TOOLS:
        func_name = tool["function"]
        assert hasattr(gurddy, func_name), f"Function {func_name} not found in gurddy handlers"


def test_server_loads_all_tools():
    """Test that MCP server loads all tools from registry."""
    server = MCPStdioServer()
    
    # Check that all tools are loaded
    assert len(server.tools) == len(TOOLS)
    
    # Check that all function mappings exist
    assert len(server.function_map) == len(TOOLS)
    
    # Check that tool names match
    registry_names = {tool["name"] for tool in TOOLS}
    server_names = set(server.tools.keys())
    assert registry_names == server_names


def test_tool_schemas_match():
    """Test that tool schemas in server match registry."""
    server = MCPStdioServer()
    
    for tool_name, schema in server.tools.items():
        tool_def = get_tool_by_name(tool_name)
        assert tool_def is not None
        assert schema["description"] == tool_def["description"]
        assert schema["inputSchema"] == tool_def["inputSchema"]


def test_function_mapping_correct():
    """Test that function mapping is correct."""
    server = MCPStdioServer()
    
    for tool_name, func in server.function_map.items():
        tool_def = get_tool_by_name(tool_name)
        expected_func_name = tool_def["function"]
        actual_func = getattr(gurddy, expected_func_name)
        assert func == actual_func, f"Function mismatch for {tool_name}"


def test_no_duplicate_tool_names():
    """Test that there are no duplicate tool names."""
    tool_names = [tool["name"] for tool in TOOLS]
    assert len(tool_names) == len(set(tool_names)), "Duplicate tool names found"


def test_tool_categories_valid():
    """Test that all tool categories are valid."""
    valid_categories = {"meta", "examples", "csp", "optimization", "game_theory", "classic", "scipy"}
    for tool in TOOLS:
        assert tool["category"] in valid_categories, f"Invalid category: {tool['category']}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
