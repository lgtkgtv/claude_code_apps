#!/usr/bin/env python3
"""
Simple run script for the Expense Tracker application
"""
import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import fastapi
        import nicegui
        import uvicorn
        import pydantic
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def main():
    """Main entry point"""
    print("🚀 Starting Expense Tracker Application...")
    
    if not check_dependencies():
        sys.exit(1)
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    try:
        # Run the main application
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Application failed with error code {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()