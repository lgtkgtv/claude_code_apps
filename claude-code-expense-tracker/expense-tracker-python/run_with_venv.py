#!/usr/bin/env python3
"""
Run script using uv
"""
import subprocess
import sys
import os

def main():
    """Main entry point"""
    # Check if uv is available
    if not subprocess.run(["which", "uv"], capture_output=True).returncode == 0:
        print("❌ uv not found!")
        print("Please install uv first or run: ./setup.sh")
        sys.exit(1)
    
    print("🚀 Starting Expense Tracker with uv...")
    
    try:
        # Run with uv
        subprocess.run(["uv", "run", "python", "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Application failed with error code {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()