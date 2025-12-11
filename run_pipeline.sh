#!/bin/bash

# -------------------------
# Strict mode
# -------------------------
set -e

# -------------------------
# 0. Load Environment Variables (API Keys)
# -------------------------
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

echo -e "\033[0;36m>>> Starting AI-Gov Framework Pipeline...\033[0m"

# -------------------------
# 1. Python Environment
# -------------------------
PYTHON="python3"

# Check if python is available
if ! command -v $PYTHON &> /dev/null; then
    echo "ERROR: 'python3' command not found."
    exit 1
fi

# -------------------------
# 2. Check SerpApi key
# -------------------------
if [ -z "$SERPAPI_KEY" ] && [ -z "$SERPAPI_API_KEY" ]; then
    echo "ERROR: SERPAPI_KEY is not set in your .env file!"
    echo "Please add SERPAPI_KEY=your_key to .env"
    exit 1
fi

# -------------------------
# 3. Run scripts (UPDATED PATHS)
# -------------------------

# Step 1: Scrape Data -> Now in 'knowledge_base'
echo ">>> Step 1: Scraping Google Scholar"
# $PYTHON knowledge_base/scrape_google_scholar.py # Uncomment once you have a API key

# Step 2: Clean Data -> Now in 'data_governance'
echo ">>> Step 2: Preprocessing Results"
$PYTHON data_governance/preprocess_results.py

# Step 3: Get PDFs -> Now in 'knowledge_base'
echo ">>> Step 3: Retrieving PDFs for keywords"
$PYTHON knowledge_base/retrieve_pdfs_keywords.py

# Step 4: Keywords -> Now in 'specialized_agents'
echo ">>> Step 4: Extracting Keywords"
$PYTHON specialized_agents/extract_keywords.py

# Step 5: Make Graph -> Now in 'specialized_agents'
echo ">>> Step 5: Generating Network Graph"
$PYTHON specialized_agents/save_network.py

# Step 6: RAG Pipeline (Download & Ingest)
echo ">>> Step 6a: Downloading PDFs for Knowledge Base"
$PYTHON knowledge_base/retrieve_pdfs.py

echo ">>> Step 6b: Ingesting PDFs into Vector Database"
$PYTHON knowledge_base/ingest_policies.py

# -------------------------
# 4. Move Outputs to Dashboard
# -------------------------
echo ">>> Copying outputs to app/assets..."
mkdir -p app/assets

# Copy the generated graph and stats so the UI can see them
cp -f data/processed/network_graph.html app/assets/network_graph.html 2>/dev/null || :
cp -f data/processed/cooccurence_network.gexf app/assets/cooccurence_network.gexf 2>/dev/null || :
cp -f data/processed/network_statistics.csv app/assets/network_statistics.csv 2>/dev/null || :
cp -f data/processed/keyword_stats.json app/assets/keyword_stats.json 2>/dev/null || :

echo -e "\033[0;32m>>> Pipeline Completed Successfully!\033[0m"
