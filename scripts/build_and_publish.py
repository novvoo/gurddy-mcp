#!/usr/bin/env python3
"""
Build and publish script for gurddy_mcp package.

Usage:
    python scripts/build_and_publish.py --test    # Upload to TestPyPI
    python scripts/build_and_publish.py --prod    # Upload to PyPI
    python scripts/build_and_publish.py --build   # Build only
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd, check=True):
    """Run a shell command."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=check)
    return result.returncode == 0


def clean_build():
    """Clean previous build artifacts."""
    print("Cleaning build artifacts...")
    run_command("rm -rf build/ dist/ *.egg-info/", check=False)


def generate_schemas():
    """Generate schemas from function signatures."""
    print("Generating schemas from function signatures...")
    return run_command("python generate_registry.py")


def build_package():
    """Build the package."""
    print("Building package...")
    return run_command("python -m build")


def upload_to_testpypi():
    """Upload to TestPyPI."""
    print("Uploading to TestPyPI...")
    return run_command("python -m twine upload --repository testpypi dist/*")


def upload_to_pypi():
    """Upload to PyPI."""
    print("Uploading to PyPI...")
    return run_command("python -m twine upload dist/*")


def run_tests():
    """Run tests before building."""
    print("Running tests...")
    return run_command("python -m pytest tests/ -v")


def check_dependencies():
    """Check if required tools are installed."""
    tools = ["build", "twine"]
    missing = []
    
    for tool in tools:
        if not run_command(f"python -m {tool} --help > /dev/null 2>&1", check=False):
            missing.append(tool)
    
    if missing:
        print(f"Missing required tools: {', '.join(missing)}")
        print("Install them with: pip install build twine")
        return False
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Build and publish gurddy_mcp package")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--build", action="store_true", help="Build package only")
    group.add_argument("--test", action="store_true", help="Build and upload to TestPyPI")
    group.add_argument("--prod", action="store_true", help="Build and upload to PyPI")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    
    args = parser.parse_args()
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    print(f"Working in: {project_root}")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Generate schemas
    if not generate_schemas():
        print("Schema generation failed!")
        sys.exit(1)
    
    # Run tests
    if not args.skip_tests:
        if not run_tests():
            print("Tests failed! Aborting.")
            sys.exit(1)
    
    # Clean and build
    clean_build()
    if not build_package():
        print("Build failed!")
        sys.exit(1)
    
    # Upload if requested
    if args.test:
        if not upload_to_testpypi():
            print("Upload to TestPyPI failed!")
            sys.exit(1)
        print("✅ Successfully uploaded to TestPyPI!")
        print("Install with: pip install -i https://test.pypi.org/simple/ gurddy-mcp")
    
    elif args.prod:
        confirm = input("Are you sure you want to upload to PyPI? (yes/no): ")
        if confirm.lower() != "yes":
            print("Upload cancelled.")
            sys.exit(0)
        
        if not upload_to_pypi():
            print("Upload to PyPI failed!")
            sys.exit(1)
        print("✅ Successfully uploaded to PyPI!")
        print("Install with: pip install gurddy_mcp")
    
    else:
        print("✅ Package built successfully!")
        print("Files in dist/:")
        run_command("ls -la dist/")


if __name__ == "__main__":
    main()