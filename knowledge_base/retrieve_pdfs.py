import os
import requests
import pandas as pd
import time
import urllib3
import random
from urllib.parse import urlparse

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
INPUT_FILE = "data/raw/google_scholar_organic_results.csv"
OUTPUT_FOLDER = "data/raw_policies"

# --- STEALTH HEADERS ---
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://scholar.google.com/",
    "Connection": "keep-alive"
}

def retrieve_pdfs():
    print(f">>> Starting PDF Retriever (Final Robust Mode)...")
    
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    try:
        df = pd.read_csv(INPUT_FILE, on_bad_lines='skip')
        print(f"    [Info] Loaded {len(df)} rows.")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    success_count = 0
    skipped_count = 0
    fail_count = 0
    
    blocked_domains = set()

    session = requests.Session()
    session.headers.update(HEADERS)

    for index, row in df.iterrows():
        title = str(row.get('title', f"doc_{index}")).strip()

        if "retracted" in title.lower():
            continue
        
        # 1. GET URL (Last Column Strategy)
        target_url = str(row.iloc[-1]).strip()
        if not target_url.lower().startswith("http"):
            target_url = str(row.iloc[-2]).strip()
            if not target_url.lower().startswith("http"):
                continue

        # CHECK BLACKLIST
        try:
            domain = urlparse(target_url).netloc
        except:
            continue # Skip invalid URLs

        if domain in blocked_domains:
            fail_count += 1
            continue

        # 2. FILENAME CHECK
        safe_filename = "".join([c for c in title if c.isalnum() or c in (' ', '_')]).rstrip()
        safe_filename = safe_filename.replace(" ", "_")[:50]
        if not safe_filename: safe_filename = f"doc_{index}"
        
        save_path = os.path.join(OUTPUT_FOLDER, f"{safe_filename}.pdf")

        if os.path.exists(save_path) and os.path.getsize(save_path) > 1024:
            print(f"  [Skip] Exists: {safe_filename}.pdf")
            skipped_count += 1
            continue

        # 3. DOWNLOAD
        try:
            print(f"  [Down] Fetching: {target_url[:50]}...", end="")
            
            response = session.get(target_url, timeout=15, verify=False, allow_redirects=True, stream=True)
            
            if response.status_code == 403:
                print(f"    -> 🚫 Access Denied (403). Adding '{domain}' to blacklist.")
                blocked_domains.add(domain)
                fail_count += 1
                time.sleep(random.uniform(1, 2)) 
                continue
            
            if response.status_code == 404:
                print(f"    -> ❌ Failed: 404 Not Found (Dead Link)")
                fail_count += 1
                continue

            content_type = response.headers.get('Content-Type', '').lower()
            is_pdf = 'application/pdf' in content_type or target_url.lower().endswith('.pdf')
            
            if is_pdf:
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"    -> ✅ Success!")
                success_count += 1
            else:
                print(f"    -> ❌ Failed: Not a PDF (Type: {content_type})")
                fail_count += 1

            time.sleep(random.uniform(1, 3))

        # --- SPECIFIC ERROR HANDLING (Clean Logs) ---
        except requests.exceptions.ConnectionError:
            # Handles NameResolutionError, MaxRetries, etc.
            print(f"    -> ❌ Failed: Connection Error (Server Down or Bad Domain)")
            fail_count += 1
        except requests.exceptions.Timeout:
            print(f"    -> ❌ Failed: Request Timed Out")
            fail_count += 1
        except requests.exceptions.RequestException as e:
            # Catch-all for other HTTP errors
            print(f"    -> ❌ Failed: HTTP/Network Error ({str(e)[:50]}...)")
            fail_count += 1
        except Exception as e:
            print(f"    -> Error: {e}")
            fail_count += 1

    print(f"\n>>> Complete. Success: {success_count} | Skipped: {skipped_count} | Failed: {fail_count}")

if __name__ == "__main__":
    retrieve_pdfs()