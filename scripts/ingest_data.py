# scripts/ingest_data.py
import subprocess
import os
import sys

def run_module(module_path):
    try:
        print(f"Running module: {module_path}...")
        subprocess.run([sys.executable, "-m", module_path], check=True)
        print(f"{module_path} completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"Failed to run {module_path}: {e}\n")

if __name__ == "__main__":
    # Move to project root (rag-chatbot/) to ensure relative imports work
    os.chdir(os.path.dirname(os.path.dirname(__file__)))

    run_module("app.ingestion.scraper")
    run_module("app.ingestion.processor")
