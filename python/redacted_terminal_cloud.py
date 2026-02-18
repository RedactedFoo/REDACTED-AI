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

    # --- Validation ---
    if not os.path.exists(script_path):
        print(f"Error: Cloud worker script not found at '{script_path}'")
        sys.exit(1)

    # --- Build Command ---
    cmd = [sys.executable, script_path]
    
    # Set environment for the subprocess to run in persistent mode
    env = os.environ.copy()
    env["MODE"] = "persistent"
    
    print(f"[main.py] Starting swarm worker in PERSISTENT mode...")
    print(f"[main.py] Executing command: {' '.join(cmd)}")
    print(f"[main.py] Environment: MODE={env['MODE']}")
    
    # Debug: Print relevant API keys that are being passed to the subprocess
    for key in ['GROQ_API_KEY', 'XAI_API_KEY', 'OPENAI_API_KEY', 'LLM_PROVIDER']:
        if key in env:
            # Only print the key and not the value for security
            print(f"[main.py] Environment: {key}=***")

    try:
        # Pass the custom 'env' to subprocess.run
        result = subprocess.run(cmd, check=True, cwd=repo_root, env=env)
        sys.exit(result.returncode)
    except subprocess.CalledProcessError as e:
        print(f"[main.py] Worker script exited with error: {e}")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print(f"[main.py] Error: The script '{script_path}' was not found or is not executable.")
        sys.exit(1)


if __name__ == "__main__":
    main()
