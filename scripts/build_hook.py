#!/usr/bin/env python3
"""
Build hook script that runs before package building.
This ensures schemas are generated and verified before building.
"""

import sys
import subprocess
import os
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Main build hook function."""
    print("🚀 Running pre-build hooks...")
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Step 1: Generate schemas
    if not run_command(f"{sys.executable} scripts/generate_registry.py", "Generating schemas"):
        sys.exit(1)
    
    # Step 2: Verify consistency
    if not run_command(f"{sys.executable} scripts/verify_consistency.py", "Verifying consistency"):
        sys.exit(1)
    
    print("🎉 All pre-build hooks completed successfully!")


if __name__ == "__main__":
    main()