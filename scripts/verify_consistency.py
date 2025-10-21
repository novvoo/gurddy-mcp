#!/usr/bin/env python3
"""Verify consistency between tool registry and server implementations."""

import sys
from mcp_server.tool_registry import TOOLS, TOOL_SCHEMAS, get_tool_by_name
from mcp_server.mcp_stdio_server import MCPStdioServer
from mcp_server.core.tool_registry import get_registry
from mcp_server.handlers import gurddy

# Import to register HTTP tools
import mcp_server.tools.registry  # noqa: F401


def verify_stdio_server():
    """Verify stdio server consistency."""
    print("🔍 Verifying Stdio Server...")
    server = MCPStdioServer()
    
    # Check tool count
    if len(server.tools) != len(TOOLS):
        print(f"  ❌ Tool count mismatch: {len(server.tools)} vs {len(TOOLS)}")
        return False
    print(f"  ✅ Tool count: {len(server.tools)}")
    
    # Check all tools are registered
    for tool in TOOLS:
        tool_name = tool["name"]
        if tool_name not in server.tools:
            print(f"  ❌ Tool '{tool_name}' not found in stdio server")
            return False
        if tool_name not in server.function_map:
            print(f"  ❌ Function mapping missing for '{tool_name}'")
            return False
    print(f"  ✅ All tools registered")
    
    # Check schemas match
    for tool_name, schema in server.tools.items():
        tool_def = get_tool_by_name(tool_name)
        if schema["description"] != tool_def["description"]:
            print(f"  ❌ Description mismatch for '{tool_name}'")
            return False
        if schema["inputSchema"] != tool_def["inputSchema"]:
            print(f"  ❌ Schema mismatch for '{tool_name}'")
            return False
    print(f"  ✅ All schemas match")
    
    return True


def verify_http_server():
    """Verify HTTP server consistency."""
    print("\n🔍 Verifying HTTP Server...")
    registry = get_registry()
    tools = registry.get_tools()
    
    # Check tool count
    if len(tools) != len(TOOLS):
        print(f"  ❌ Tool count mismatch: {len(tools)} vs {len(TOOLS)}")
        return False
    print(f"  ✅ Tool count: {len(tools)}")
    
    # Check all tools are registered
    for tool in TOOLS:
        tool_name = tool["name"]
        if tool_name not in tools:
            print(f"  ❌ Tool '{tool_name}' not found in HTTP server")
            return False
    print(f"  ✅ All tools registered")
    
    # Check handlers exist
    for tool in TOOLS:
        handler = registry.get_handler(tool["name"])
        if handler is None:
            print(f"  ❌ Handler missing for '{tool['name']}'")
            return False
    print(f"  ✅ All handlers exist")
    
    return True


def verify_handlers():
    """Verify all handler functions exist."""
    print("\n🔍 Verifying Handler Functions...")
    
    for tool in TOOLS:
        func_name = tool["function"]
        if not hasattr(gurddy, func_name):
            print(f"  ❌ Handler function '{func_name}' not found")
            return False
    print(f"  ✅ All {len(TOOLS)} handler functions exist")
    
    return True


def verify_schemas():
    """Verify all tools have valid schemas."""
    print("\n🔍 Verifying Tool Schemas...")
    
    for tool in TOOLS:
        # Check required fields
        required_fields = ["name", "function", "description", "category", "module", "inputSchema"]
        for field in required_fields:
            if field not in tool:
                print(f"  ❌ Tool '{tool.get('name', 'unknown')}' missing field '{field}'")
                return False
        
        # Check inputSchema structure
        schema = tool["inputSchema"]
        if "type" not in schema or schema["type"] != "object":
            print(f"  ❌ Tool '{tool['name']}' has invalid inputSchema type")
            return False
        if "properties" not in schema:
            print(f"  ❌ Tool '{tool['name']}' missing properties in inputSchema")
            return False
        if "required" not in schema:
            print(f"  ❌ Tool '{tool['name']}' missing required in inputSchema")
            return False
    
    print(f"  ✅ All {len(TOOLS)} schemas are valid")
    return True


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("Tool Registry Consistency Verification")
    print("=" * 60)
    
    checks = [
        ("Schemas", verify_schemas),
        ("Handlers", verify_handlers),
        ("Stdio Server", verify_stdio_server),
        ("HTTP Server", verify_http_server),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All consistency checks passed!")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
