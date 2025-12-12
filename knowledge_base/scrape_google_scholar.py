import os
import sys
import pandas as pd
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Load API Key
load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY") or os.getenv("SERPAPI_API_KEY")

# Configuration
QUERY = "AI Governance Frameworks"  # You can change this query
OUTPUT_FILE = "data/raw/google_scholar_organic_results.csv"

def scrape_scholar():
    if not API_KEY:
        print("❌ Error: SERPAPI_KEY not found in .env")
        return

    print(f">>> Scraping Google Scholar for: '{QUERY}'...")
    
    params = {
        "engine": "google_scholar",
        "q": QUERY,
        "api_key": API_KEY,
        "num": 10  # Number of results to fetch
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        organic_results = results.get("organic_results", [])
        
        if not organic_results:
            print("⚠️ Warning: No organic results returned from SerpApi.")
            print(f"Debug Message: {results.get('error')}")
            return

        # Extract only relevant columns
        cleaned_data = []
        for item in organic_results:
            cleaned_data.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet"),
                "publication_info": item.get("publication_info", {}).get("summary", "")
            })

        # Save to CSV
        df = pd.DataFrame(cleaned_data)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"✅ Success! Saved {len(df)} results to {OUTPUT_FILE}")
        print(df.head(1)) # Show the first row to verify

    except Exception as e:
        print(f"❌ Critical Error during scraping: {e}")
        sys.exit(1)


if __name__ == "__main__":
    scrape_scholar()
