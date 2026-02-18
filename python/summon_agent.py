#!/usr/bin/env python3
"""
Main entrypoint for deploying the REDACTED AI Swarm worker on Railway.
"""
import os
import subprocess
import sys

# --- Configuration ---
# The cloud script is designed to handle various LLM providers
WORKER_SCRIPT = "python/redacted_terminal_cloud.py"

def main():
    """
    Builds and executes the command to run the swarm worker using the cloud script.
    """
    repo_root = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(repo_root, WORKER_SCRIPT)
    agent_path = os.path.join(repo_root, "agents", "RedactedIntern.character.json")

    # --- Validation ---
    if not os.path.exists(script_path):
        print(f"Error: Cloud worker script not found at '{script_path}'")
        sys.exit(1)

    if not os.path.exists(agent_path):
        print(f"Error: Agent file not found at '{agent_path}'")
        sys.exit(1)

    # --- Build Command ---
    # The cloud script uses a simple loop to run the agent in persistent mode
    cmd = [sys.executable, script_path]
    
    print(f"[main.py] Starting swarm worker with cloud script...")
    print(f"[main.py] Executing command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True, cwd=repo_root)
        sys.exit(result.returncode)
    except subprocess.CalledProcessError as e:
        print(f"[main.py] Worker script exited with error: {e}")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print(f"[main.py] Error: The script '{script_path}' was not found or is not executable.")
        sys.exit(1)


if __name__ == "__main__":
    main()

