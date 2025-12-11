import os
import requests
import pandas as pd
import time
import urllib3

# Suppress SSL warnings (common when scraping)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
INPUT_FILE = "data/raw/google_scholar_organic_results.csv"
OUTPUT_FOLDER = "data/raw_policies"

def retrieve_pdfs():
    print(f">>> Starting Smart PDF Retriever...")
    print(f"    Reading: {INPUT_FILE}")
    print(f"    Saving to: {OUTPUT_FOLDER}")

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Load Data
    try:
        df = pd.read_csv(INPUT_FILE, on_bad_lines='skip') # Skip malformed rows
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    success_count = 0
    
    # Iterate through every row
    for index, row in df.iterrows():
        title = str(row.get('title', f"doc_{index}")).strip()
        
        # --- LOGIC: Find the best link ---
        # 1. Start with the standard 'link' column
        target_url = row.get('link', '')
        
        # 2. Check if ANY column in this row has a direct .pdf link
        # This fixes the issue where the PDF link is at the end of the CSV
        pdf_candidate = None
        for col_value in row.values:
            val_str = str(col_value).strip()
            if val_str.lower().startswith("http") and val_str.lower().endswith(".pdf"):
                pdf_candidate = val_str
                break  # Found a direct PDF!
        
        # If we found a direct PDF link, OVERRIDE the target_url
        if pdf_candidate:
            target_url = pdf_candidate
            print(f"  [Info] Found Direct PDF link for '{title[:20]}...'")
        
        # Skip if no URL found
        if not target_url or str(target_url).lower() == 'nan':
            continue

        # --- FILENAME SANITIZATION ---
        safe_filename = "".join([c for c in title if c.isalnum() or c in (' ', '_')]).rstrip()
        safe_filename = safe_filename.replace(" ", "_")[:50]
        if not safe_filename:
            safe_filename = f"doc_{index}"
        
        save_path = os.path.join(OUTPUT_FOLDER, f"{safe_filename}.pdf")

        if os.path.exists(save_path):
            print(f"  [Skip] Exists: {safe_filename}.pdf")
            continue

        # --- DOWNLOAD ---
        try:
            print(f"  [Down] Fetching: {target_url}...")
            
            # Browser Headers (Critical for sites like ResearchGate/IEEE)
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            }
            
            # Streaming download to handle large files
            response = requests.get(target_url, headers=headers, timeout=15, verify=False, stream=True)
            
            # Check if valid
            content_type = response.headers.get('Content-Type', '').lower()
            
            # Logic: If URL ends in PDF OR Header says PDF
            if 'application/pdf' in content_type or target_url.endswith('.pdf'):
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"    -> ✅ Success!")
                success_count += 1
            else:
                print(f"    -> ❌ Failed: Content-Type is '{content_type}' (likely a landing page)")

            time.sleep(1) # Be polite

        except Exception as e:
            print(f"    -> Error: {e}")

    print(f"\n>>> Retrieval Complete. Downloaded {success_count} PDFs.")

if __name__ == "__main__":
    retrieve_pdfs()
