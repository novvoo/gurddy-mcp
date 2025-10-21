"""
Test tool registry system integrity.
"""

import pytest
from mcp_server.tool_registry import (
    TOOLS,
    TOOL_COUNT,
    get_all_tool_names,
    get_all_function_names,
    get_categories,
    get_tools_by_category,
)
from mcp_server import __all__ as exported_functions
import mcp_server.handlers.gurddy as gurddy_module


def test_tool_count():
    """Test that tool count matches the number of tools."""
    assert TOOL_COUNT == len(TOOLS)
    assert TOOL_COUNT > 0


def test_all_tools_have_required_fields():
    """Test that all tools have required fields."""
    required_fields = {"name", "function", "description", "category", "module"}
    for tool in TOOLS:
        assert required_fields.issubset(tool.keys()), f"Tool {tool.get('name')} missing required fields"


def test_tool_names_unique():
    """Test that all tool names are unique."""
    names = [tool["name"] for tool in TOOLS]
    assert len(names) == len(set(names)), "Duplicate tool names found"


def test_function_names_exist_in_modules():
    """Test that all registered functions exist in their specified modules."""
    import importlib
    for tool in TOOLS:
        func_name = tool["function"]
        module_path = f"mcp_server.{tool['module']}"
        try:
            module = importlib.import_module(module_path)
            assert hasattr(module, func_name), f"Function {func_name} not found in {module_path}"
        except ImportError:
            pytest.fail(f"Module {module_path} not found for function {func_name}")


def test_all_functions_exported():
    """Test that all registered functions are exported from __init__.py"""
    function_names = set(get_all_function_names())
    exported = set(exported_functions)
    
    # All registered functions should be exported (plus solve_csp_generic)
    assert function_names.issubset(exported), f"Missing exports: {function_names - exported}"


def test_categories_valid():
    """Test that all categories are valid."""
    valid_categories = {"meta", "examples", "csp", "optimization", "game_theory", "scipy", "classic"}
    categories = get_categories()
    for category in categories:
        assert category in valid_categories, f"Invalid category: {category}"


def test_get_tools_by_category():
    """Test filtering tools by category."""
    for category in get_categories():
        tools = get_tools_by_category(category)
        assert len(tools) > 0, f"No tools found for category {category}"
        for tool in tools:
            assert tool["category"] == category


def test_tool_descriptions_not_empty():
    """Test that all tools have non-empty descriptions."""
    for tool in TOOLS:
        assert tool["description"].strip(), f"Tool {tool['name']} has empty description"


def test_registry_consistency():
    """Test that registry data is consistent."""
    assert len(get_all_tool_names()) == TOOL_COUNT
    assert len(get_all_function_names()) == TOOL_COUNT


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
