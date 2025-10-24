#!/usr/bin/env python3
"""
Simple script to generate tool_registry.py with auto-generated schemas.
"""

import inspect
import importlib
import sys
import os
from pathlib import Path
from typing import Dict, Any, get_type_hints, Union, Optional, List
import json

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mcp_server.tool_definitions import TOOL_DEFINITIONS


def get_type_schema(type_hint: Any) -> Dict[str, Any]:
    """Convert Python type hint to JSON schema."""
    if type_hint == str:
        return {"type": "string"}
    elif type_hint == int:
        return {"type": "integer"}
    elif type_hint == float:
        return {"type": "number"}
    elif type_hint == bool:
        return {"type": "boolean"}
    elif type_hint == list or type_hint == List:
        return {"type": "array"}
    elif type_hint == dict or type_hint == Dict:
        return {"type": "object"}
    
    # Handle Union types (Optional is Union[T, None])
    if hasattr(type_hint, '__origin__'):
        if type_hint.__origin__ is Union:
            args = type_hint.__args__
            if len(args) == 2 and type(None) in args:
                non_none_type = args[0] if args[1] is type(None) else args[1]
                return get_type_schema(non_none_type)
        elif type_hint.__origin__ is list:
            if type_hint.__args__:
                item_schema = get_type_schema(type_hint.__args__[0])
                return {"type": "array", "items": item_schema}
            return {"type": "array"}
        elif type_hint.__origin__ is dict:
            return {"type": "object"}
    
    return {"type": "object"}


def generate_schema(module_name: str, function_name: str) -> Dict[str, Any]:
    """Generate JSON schema from function signature."""
    try:
        module = importlib.import_module(f"mcp_server.{module_name}")
        func = getattr(module, function_name)
        
        sig = inspect.signature(func)
        type_hints = get_type_hints(func)
        
        properties = {}
        required = []
        
        for param_name, param in sig.parameters.items():
            if param_name in type_hints:
                param_schema = get_type_schema(type_hints[param_name])
            else:
                param_schema = {"type": "string"}
            
            param_schema["description"] = f"Parameter {param_name}"
            properties[param_name] = param_schema
            
            if param.default is inspect.Parameter.empty:
                required.append(param_name)
        
        return {
            "type": "object",
            "properties": properties,
            "required": required
        }
        
    except Exception as e:
        print(f"Error generating schema for {module_name}.{function_name}: {e}")
        return {"type": "object", "properties": {}, "required": []}


def main():
    print("🔄 Generating tool registry with auto-generated schemas...")
    
    # Change to project root directory
    os.chdir(project_root)
    
    tools = []
    for tool_def in TOOL_DEFINITIONS:
        schema = generate_schema(tool_def["module"], tool_def["function"])
        
        tool = tool_def.copy()
        tool["inputSchema"] = schema
        tools.append(tool)
        
        print(f"✅ {tool_def['name']}")
    
    # Generate registry content
    tools_json = json.dumps(tools, indent=4, ensure_ascii=False)
    
    registry_content = f'''"""
Central registry for all MCP tools and their metadata.
This is the single source of truth for tool definitions.

NOTE: Schemas are auto-generated from function signatures.
Run `python scripts/generate_registry.py` to update.
"""

from typing import List, Dict, Any

# Tool definitions - single source of truth
# Schemas auto-generated from function signatures
TOOLS = {tools_json}


def get_all_tool_names() -> List[str]:
    """Get list of all tool names."""
    return [tool["name"] for tool in TOOLS]


def get_all_function_names() -> List[str]:
    """Get list of all function names for imports."""
    return [tool["function"] for tool in TOOLS]


def get_tools_by_category(category: str) -> List[Dict[str, Any]]:
    """Get tools filtered by category."""
    return [tool for tool in TOOLS if tool["category"] == category]


def get_tool_count() -> int:
    """Get total number of tools."""
    return len(TOOLS)


def get_categories() -> List[str]:
    """Get list of all categories."""
    return list(set(tool["category"] for tool in TOOLS))


def get_tool_schemas() -> Dict[str, Dict[str, Any]]:
    """Get tool schemas for MCP server registration.
    
    Returns:
        Dict mapping tool name to schema (description + inputSchema)
    """
    schemas = {{}}
    for tool in TOOLS:
        schemas[tool["name"]] = {{
            "description": tool["description"],
            "inputSchema": tool["inputSchema"]
        }}
    return schemas


def get_tool_by_name(name: str) -> Dict[str, Any]:
    """Get tool definition by name."""
    for tool in TOOLS:
        if tool["name"] == name:
            return tool
    return None


def get_function_name_mapping() -> Dict[str, str]:
    """Get mapping from tool name to function name.
    
    Returns:
        Dict mapping tool name to function name
    """
    return {{tool["name"]: tool["function"] for tool in TOOLS}}


def generate_tool_list_markdown() -> str:
    """Generate markdown list of all tools for documentation."""
    lines = []
    for tool in TOOLS:
        lines.append(f"- `{{tool['name']}}` - {{tool['description']}}")
    return "\\n".join(lines)


def generate_auto_approve_list() -> List[str]:
    """Generate list of tool names for MCP auto-approve configuration."""
    return get_all_tool_names()


# Export commonly used values
ALL_TOOL_NAMES = get_all_tool_names()
ALL_FUNCTION_NAMES = get_all_function_names()
TOOL_COUNT = get_tool_count()
TOOL_SCHEMAS = get_tool_schemas()
FUNCTION_NAME_MAPPING = get_function_name_mapping()
'''
    
    # Write to file (relative to project root)
    registry_path = project_root / "mcp_server" / "tool_registry.py"
    with open(registry_path, 'w', encoding='utf-8') as f:
        f.write(registry_content)
    
    print(f"\n🎉 Generated tool_registry.py with {len(tools)} tools")
    print("💡 Run 'python scripts/verify_consistency.py' to verify the generated registry")


if __name__ == "__main__":
    main()