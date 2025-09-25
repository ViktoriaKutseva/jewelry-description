#!/usr/bin/env python3
"""
Startup script for the jewelry web application.
Simple wrapper to run the Clean Architecture web application.
"""
import subprocess
import sys
import os

if __name__ == "__main__":
    print("🏺 Starting Jewelry Cost Calculator Web Server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("🔗 Open your browser and navigate to the URL above")
    print("⌨️  Press Ctrl+C to stop the server")
    print()
    
    # Change to project directory (parent of scripts)
    project_dir = os.path.dirname(os.path.dirname(__file__))
    os.chdir(project_dir)
    
    # Use virtual environment Python if available, otherwise system python
    python_cmd = os.path.join(project_dir, ".venv", "bin", "python")
    if not os.path.exists(python_cmd):
        python_cmd = sys.executable
    
    # Run the application as a module
    try:
        subprocess.run([
            python_cmd, 
            "-m", 
            "jewelry_description.entrypoints.web.main"
        ], check=True, cwd="src")
    except KeyboardInterrupt:
        print("\n✅ Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running server: {e}")
        sys.exit(1)