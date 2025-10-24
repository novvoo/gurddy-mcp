#!/usr/bin/env python3
"""
Schema consistency validator for MCP tools.
Validates that tool schemas match their actual function signatures.
"""

import inspect
import importlib
import sys
from pathlib import Path
from typing import Dict, List, Any, Set

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mcp_server.tool_registry import TOOLS


def get_function_signature_params(module_name: str, function_name: str) -> Set[str]:
    """Get parameter names from function signature."""
    try:
        module = importlib.import_module(f"mcp_server.{module_name}")
        func = getattr(module, function_name)
        sig = inspect.signature(func)
        return set(sig.parameters.keys())
    except Exception as e:
        print(f"Error importing {module_name}.{function_name}: {e}")
        return set()


def get_schema_params(input_schema: Dict[str, Any]) -> Set[str]:
    """Get parameter names from JSON schema."""
    properties = input_schema.get("properties", {})
    return set(properties.keys())


def validate_tool_consistency() -> List[Dict[str, Any]]:
    """Validate consistency between tool schemas and function signatures."""
    inconsistencies = []
    
    for tool in TOOLS:
        tool_name = tool["name"]
        module_name = tool["module"]
        function_name = tool["function"]
        input_schema = tool["inputSchema"]
        
        # Get parameter names from both sources
        schema_params = get_schema_params(input_schema)
        function_params = get_function_signature_params(module_name, function_name)
        
        if not function_params:
            # Skip if we couldn't load the function
            continue
            
        # Check for mismatches
        missing_in_schema = function_params - schema_params
        extra_in_schema = schema_params - function_params
        
        if missing_in_schema or extra_in_schema:
            inconsistencies.append({
                "tool_name": tool_name,
                "module": module_name,
                "function": function_name,
                "missing_in_schema": list(missing_in_schema),
                "extra_in_schema": list(extra_in_schema),
                "schema_params": list(schema_params),
                "function_params": list(function_params)
            })
    
    return inconsistencies


def main():
    """Main validation function."""
    print("🔍 Validating MCP tool schema consistency...")
    
    inconsistencies = validate_tool_consistency()
    
    if not inconsistencies:
        print("✅ All tool schemas are consistent with their function signatures!")
        return 0
    
    print(f"❌ Found {len(inconsistencies)} inconsistencies:")
    print()
    
    for issue in inconsistencies:
        print(f"Tool: {issue['tool_name']}")
        print(f"  Function: {issue['module']}.{issue['function']}")
        print(f"  Schema params: {issue['schema_params']}")
        print(f"  Function params: {issue['function_params']}")
        
        if issue['missing_in_schema']:
            print(f"  ⚠️  Missing in schema: {issue['missing_in_schema']}")
        
        if issue['extra_in_schema']:
            print(f"  ⚠️  Extra in schema: {issue['extra_in_schema']}")
        
        print()
    
    return 1


if __name__ == "__main__":
    exit(main())