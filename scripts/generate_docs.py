#!/usr/bin/env python3
"""
Generate documentation snippets from tool registry.
Run this script to update documentation when tools are added/modified.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_server.tool_registry import (
    TOOLS,
    TOOL_COUNT,
    generate_tool_list_markdown,
    generate_auto_approve_list,
)


def generate_readme_tool_list():
    """Generate the tool list section for README.md"""
    print("=" * 60)
    print(f"MCP TOOLS LIST ({TOOL_COUNT} tools)")
    print("=" * 60)
    print()
    print(generate_tool_list_markdown())
    print()


def generate_mcp_config():
    """Generate the autoApprove list for MCP configuration"""
    print("=" * 60)
    print("MCP CONFIG - autoApprove list")
    print("=" * 60)
    print()
    print('"autoApprove": [')
    tools = generate_auto_approve_list()
    for i, tool in enumerate(tools):
        comma = "," if i < len(tools) - 1 else ""
        print(f'  "{tool}"{comma}')
    print("]")
    print()


def generate_tool_summary():
    """Generate a summary of tools by category"""
    from mcp_server.tool_registry import get_categories, get_tools_by_category
    
    print("=" * 60)
    print("TOOLS BY CATEGORY")
    print("=" * 60)
    print()
    
    for category in sorted(get_categories()):
        tools = get_tools_by_category(category)
        print(f"\n{category.upper()} ({len(tools)} tools):")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")
    print()


def main():
    """Generate all documentation snippets"""
    print("\n" + "=" * 60)
    print("GURDDY MCP DOCUMENTATION GENERATOR")
    print("=" * 60 + "\n")
    
    generate_readme_tool_list()
    generate_mcp_config()
    generate_tool_summary()
    
    print("=" * 60)
    print("Copy the sections above to update:")
    print("  - README.md (tool list)")
    print("  - README.md (MCP configuration examples)")
    print("=" * 60)


if __name__ == "__main__":
    main()
