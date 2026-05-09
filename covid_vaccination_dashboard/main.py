#!/usr/bin/env python3
"""
COVID-19 Vaccination Dashboard - Main Entry Point
===============================================

This script serves as the main entry point for the COVID-19 Vaccination
Dashboard project. It provides options to run the EDA analysis or launch
the interactive dashboard.

Usage:
    python main.py --eda        # Run EDA analysis
    python main.py --dashboard  # Launch Streamlit dashboard
    python main.py --help       # Show help information

Author: COVID Vaccination Analysis Team
Date: 2024
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path

def run_eda():
    """
    Launch the Jupyter notebook for EDA analysis.
    """
    script_dir = Path(__file__).parent
    notebook_path = script_dir / "notebooks" / "eda_analysis.ipynb"
    if notebook_path.exists():
        print("Launching Jupyter notebook for EDA analysis...")
        try:
            subprocess.run(["jupyter", "notebook", str(notebook_path)], check=True)
        except subprocess.CalledProcessError:
            print("Error: Could not launch Jupyter notebook.")
            print("Make sure Jupyter is installed: pip install jupyter")
        except FileNotFoundError:
            print("Error: Jupyter command not found.")
            print("Make sure Jupyter is installed and in your PATH.")
    else:
        print(f"Error: Notebook file not found at {notebook_path}")

def run_dashboard():
    """
    Launch the Streamlit dashboard.
    """
    script_dir = Path(__file__).parent
    dashboard_path = script_dir / "dashboard" / "app.py"
    if dashboard_path.exists():
        print("Launching Streamlit dashboard...")
        try:
            subprocess.run([sys.executable, "-m", "streamlit", "run", str(dashboard_path)], check=True)
        except subprocess.CalledProcessError:
            print("Error: Could not launch Streamlit dashboard.")
            print("Make sure Streamlit is installed: pip install streamlit")
        except FileNotFoundError:
            print("Error: Streamlit command not found.")
            print("Make sure Streamlit is installed and in your PATH.")
    else:
        print(f"Error: Dashboard file not found at {dashboard_path}")

def show_help():
    """
    Display help information.
    """
    help_text = """
COVID-19 Vaccination Dashboard - Main Script

Options:
  --eda        Launch Jupyter notebook for exploratory data analysis
  --dashboard  Launch the interactive Streamlit dashboard
  --help       Show this help message

Examples:
  python main.py --eda
  python main.py --dashboard

Make sure all dependencies are installed:
  pip install -r requirements.txt
"""
    print(help_text)

def main():
    """
    Main function to parse arguments and execute appropriate action.
    """
    parser = argparse.ArgumentParser(description="COVID-19 Vaccination Dashboard")
    parser.add_argument("--eda", action="store_true", help="Run EDA analysis")
    parser.add_argument("--dashboard", action="store_true", help="Launch dashboard")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        show_help()
    elif args.eda:
        run_eda()
    elif args.dashboard:
        run_dashboard()
    else:
        print("Invalid option. Use --help for usage information.")

if __name__ == "__main__":
    main()