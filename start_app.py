#!/usr/bin/env python3
"""
Script to start both backend and frontend simultaneously
"""

import subprocess
import sys
import os
import threading
import time
import signal
import atexit
from pathlib import Path


# Global variable to store child processes
child_processes = []


def cleanup():
    """Clean up child processes on exit"""
    global child_processes
    for proc in child_processes:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        except Exception:
            pass  # Process already terminated


def run_backend():
    """Run the FastAPI backend server"""
    try:
        # Change to backend directory
        backend_dir = Path(__file__).parent / "backend"
        os.chdir(backend_dir)
        
        # Run uvicorn server
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000",
            "--reload"
        ]
        print("Starting backend server...")
        backend_process = subprocess.Popen(cmd)
        child_processes.append(backend_process)
        backend_process.wait()
    except KeyboardInterrupt:
        print("\nBackend server stopped.")
    finally:
        if backend_process in child_processes:
            child_processes.remove(backend_process)


def run_frontend():
    """Run the Streamlit frontend"""
    try:
        # Change to workspace root directory
        workspace_dir = Path(__file__).parent
        os.chdir(workspace_dir)
        
        # Run streamlit
        cmd = [sys.executable, "-m", "streamlit", "run", "streamlit_frontend.py", "--server.port=8501"]
        print("Starting frontend server...")
        frontend_process = subprocess.Popen(cmd)
        child_processes.append(frontend_process)
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nFrontend server stopped.")
    finally:
        if frontend_process in child_processes:
            child_processes.remove(frontend_process)


def main():
    """Main function to start both servers"""
    print("Starting Wishlist Application...")
    print("Backend will run on http://127.0.0.1:8000")
    print("Frontend will run on http://127.0.0.1:8501")
    print("Press Ctrl+C to stop the application")
    
    # Register cleanup function
    atexit.register(cleanup)
    
    # Handle SIGTERM
    signal.signal(signal.SIGTERM, lambda signum, frame: cleanup())
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Give backend some time to start
    time.sleep(2)
    
    # Run frontend in main thread
    run_frontend()


if __name__ == "__main__":
    main()