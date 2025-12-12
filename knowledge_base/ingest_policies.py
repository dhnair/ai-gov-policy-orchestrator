import os
import chromadb
from chromadb.config import Settings
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError

# --- CONFIGURATION ---
POLICY_FOLDER = "data/raw_policies"
DB_PATH = "data/chroma_db"
COLLECTION_NAME = "policy_knowledge_base"

def ingest_policies():
    print(f">>> Knowledge Base loading from {DB_PATH}")
    
    # Initialize ChromaDB
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

    print(f"\n>>> Scanning '{POLICY_FOLDER}' for policies...")
    
    if not os.path.exists(POLICY_FOLDER):
        print(f"Error: Policy folder '{POLICY_FOLDER}' does not exist.")
        return

    files = [f for f in os.listdir(POLICY_FOLDER) if f.lower().endswith(".pdf")]
    print(f"Found {len(files)} PDFs. Starting ingestion...")

    success_count = 0
    fail_count = 0

    for filename in files:
        file_path = os.path.join(POLICY_FOLDER, filename)
        
        try:
            print(f"Processing: {filename}...", end="", flush=True)
            
            # 1. Read PDF (with error handling)
            try:
                # strict=False allows PyPDF2 to ignore minor formatting errors
                reader = PdfReader(file_path, strict=False)
                text = ""
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
            
            except (PdfReadError, ValueError) as e:
                print(f" ❌ Corrupt PDF (EOF/Format Error). Skipping.")
                fail_count += 1
                continue
            except Exception as e:
                print(f" ❌ Unknown Error: {e}")
                fail_count += 1
                continue

            # 2. Validation (Skip empty files)
            if not text or len(text) < 50:
                print(f" ⚠️  Skipped (No readable text found).")
                fail_count += 1
                continue

            # 3. Chunking (Simple splitting by paragraphs or size)
            # For a real system, use a recursive character splitter (e.g., from LangChain)
            # Here we keep it simple: 1000 char chunks with overlap
            chunk_size = 1000
            overlap = 100
            chunks = []
            
            for i in range(0, len(text), chunk_size - overlap):
                chunk = text[i:i + chunk_size]
                if len(chunk) > 50: # Only keep substantial chunks
                    chunks.append(chunk)

            if not chunks:
                print(f" ⚠️  No valid chunks created.")
                fail_count += 1
                continue

            # 4. Add to Vector DB
            # We use filename + index as the unique ID
            ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
            metadatas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]

            collection.upsert(
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f" ✅ Indexed {len(chunks)} chunks.")
            success_count += 1

        except Exception as e:
            print(f"\n❌ Critical Error processing {filename}: {e}")
            fail_count += 1

    print(f"\n>>> Ingestion Complete.")
    print(f"    Success: {success_count}")
    print(f"    Failed:  {fail_count}")

if __name__ == "__main__":
    ingest_policies()