#!/usr/bin/env python3
"""
Quick Commands for Financial Data Parser
All-in-one script to run different components
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command with description"""
    print(f"\n🚀 {description}")
    print(f"Command: {cmd}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success!")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ Error!")
            if result.stderr:
                print(result.stderr)
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    print("🏦 FINANCIAL DATA PARSER - QUICK COMMANDS 💰")
    print("=" * 60)
    
    commands = [
        ("python test_phase1.py", "Phase 1: Basic Excel Processing Test"),
        ("python test_commands_phase1.py", "Phase 2: Component Tests"),
        ("python quick_analysis.py", "Phase 3: Quick Financial Analysis"),
        ("python full_analysis.py", "Phase 4: Complete Analysis"),
        ("streamlit run dashboard.py", "Launch Interactive Dashboard"),
        ("python cli.py --phase 1", "CLI: Run Phase 1"),
        ("python cli.py --phase 4 --report", "CLI: Full Analysis with Report"),
    ]
    
    print("Available commands:")
    for i, (cmd, desc) in enumerate(commands, 1):
        print(f"{i}. {desc}")
    
    choice = input("\nEnter command number (1-7) or 'all' for all: ").strip()
    
    if choice.lower() == 'all':
        for cmd, desc in commands:
            if 'streamlit' not in cmd:  # Skip streamlit in batch mode
                run_command(cmd, desc)
    elif choice.isdigit() and 1 <= int(choice) <= len(commands):
        cmd, desc = commands[int(choice) - 1]
        run_command(cmd, desc)
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
