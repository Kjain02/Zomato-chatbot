import subprocess
import sys
import os
# Add the project root (rag_chatbot) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# print("Current sys.path:", sys.path)

def run_script(script_name):
    try:
        print(f"Running {script_name}...")
        subprocess.run(["python", script_name], check=True)
        print(f"{script_name} completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")

def main():
    run_script("app\\ingestion\\scraper.py")
    run_script("app\\ingestion\\processor.py")  # assuming json_to_text.py is the processor

if __name__ == "__main__":
    main()
