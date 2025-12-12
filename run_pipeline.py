import os
import sys
import subprocess
import shutil
from pathlib import Path

# Try to load dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def print_step(message):
    print(f"\n\033[0;36m>>> {message}\033[0m")

def run_command(command):
    """Runs a command and stops the pipeline if it fails."""
    try:
        if command[0] == "python":
            command[0] = sys.executable
        subprocess.run(command, check=True, shell=False)
    except subprocess.CalledProcessError:
        print(f"\n\033[0;31m❌ Error occurred while running: {' '.join(command)}\033[0m")
        sys.exit(1)

def run_scraper_with_fallback():
    """
    Attempts to scrape. If it fails (API error/expired key), 
    it falls back to local data instead of crashing.
    """
    cmd = [sys.executable, "knowledge_base/scrape_google_scholar.py"]
    csv_path = Path("data/raw/google_scholar_organic_results.csv")
    
    # Check if we even have an API key configured
    api_key = os.getenv("SERPAPI_KEY") or os.getenv("SERPAPI_API_KEY")
    
    try:
        if not api_key:
            raise Exception("No API Key configured in .env")

        print("   [Attempting to scrape via SerpApi...]")
        # check=True will raise CalledProcessError if the script exits with status 1
        subprocess.run(cmd, check=True, shell=False)
        print("   [Success] Fresh data acquired.")

    except (subprocess.CalledProcessError, Exception) as e:
        # SCRAPER FAILED. Now we check for the safety net.
        print(f"\n\033[0;33m⚠️  Scraping Failed or Skipped (Reason: {e})\033[0m")
        
        if csv_path.exists() and csv_path.stat().st_size > 0:
            print(f"\033[0;32m✅ FALLBACK SUCCESS: Found existing data at {csv_path}\033[0m")
            print("   Continuing pipeline using cached data...")
            return # This counts as "Success" because we have data to work with
        else:
            # NO API + NO DATA = CRASH
            print("\n\033[0;31m❌ CRITICAL FAILURE: Scraper failed and no local cache found.\033[0m")
            print("   Please fix your API key or restore a backup CSV file.")
            sys.exit(1)

def copy_assets():
    print_step("Copying outputs to app/assets...")
    dest_dir = Path("app/assets")
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    files_map = {
        "data/processed/network_graph.html": "network_graph.html",
        "data/processed/cooccurence_network.gexf": "cooccurence_network.gexf",
        "data/processed/network_statistics.csv": "network_statistics.csv",
        "data/processed/keyword_stats.json": "keyword_stats.json"
    }
    
    for src, dest in files_map.items():
        if Path(src).exists():
            shutil.copy2(Path(src), dest_dir / dest)

    # Also copy the generated lib folder if pyvis created one
    generated_lib = Path("lib")
    if generated_lib.exists():
        if (dest_dir / "lib").exists():
            shutil.rmtree(dest_dir / "lib") # Clear old one
        shutil.copytree(generated_lib, dest_dir / "lib")
        print("   [+] Moved generated 'lib' to app/assets/lib")


def main():
    print_step("Starting AI-Gov Framework Pipeline (Resilient Mode)...")

    # 1. SPECIAL STEP: Scrape with Fallback
    print_step("Step 1: Scraping Google Scholar")
    run_scraper_with_fallback()

    # 2. STANDARD STEPS: Processing
    # These steps operate on the data (whether fresh or cached)
    steps = [
        ("Step 2: Preprocessing Results",   ["python", "data_governance/preprocess_results.py"]),
        ("Step 3: Retrieving Keywords",     ["python", "knowledge_base/retrieve_pdfs_keywords.py"]),
        ("Step 4: Extracting Keywords",     ["python", "specialized_agents/extract_keywords.py"]),
        ("Step 5: Generating Network Graph",["python", "specialized_agents/save_network.py"]),
        ("Step 6a: Downloading PDFs",       ["python", "knowledge_base/retrieve_pdfs.py"]),
        ("Step 6b: Ingesting into Vector DB",["python", "knowledge_base/ingest_policies.py"]),
    ]

    for title, cmd in steps:
        print_step(title)
        run_command(cmd)

    # 3. Finalize
    copy_assets()
    print("\n\033[0;32m>>> Pipeline Completed Successfully! 🚀\033[0m")

if __name__ == "__main__":
    main()