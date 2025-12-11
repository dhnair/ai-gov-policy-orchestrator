import os
import PyPDF2
from vector_store import PolicyKnowledgeBase

class PolicyIngestor:
    """
    Reads official government PDFs and stores them in the Vector DB.
    Implements the 'Canonical Document Store' requirement [Chapter 4.2].
    """
    def __init__(self, pdf_folder="./data/raw_policies"):
        self.pdf_folder = pdf_folder
        self.kb = PolicyKnowledgeBase()
        
        # Ensure the folder exists
        if not os.path.exists(self.pdf_folder):
            os.makedirs(self.pdf_folder)
            print(f">>> Created folder '{self.pdf_folder}'. Please put PDF files here!")

    def ingest_all(self):
        print(f"\n>>> Scanning '{self.pdf_folder}' for policies...")
        
        files = [f for f in os.listdir(self.pdf_folder) if f.endswith(".pdf")]
        
        if not files:
            print("No PDFs found! Add some .pdf files to the folder and run this again.")
            return

        for filename in files:
            self._process_pdf(filename)

    def _process_pdf(self, filename):
        file_path = os.path.join(self.pdf_folder, filename)
        print(f"Processing: {filename}...")
        
        try:
            # 1. Read the PDF
            text_content = ""
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text_content += page.extract_text() + "\n"
            
            # 2. Chunking (Simple version: split by paragraphs or strict length)
            # For this prototype, we'll index the whole text (or first 1000 chars if huge)
            # In production, use 'RecursiveCharacterTextSplitter' from LangChain
            searchable_chunk = text_content[:2000] 
            
            # 3. Add to Knowledge Base
            self.kb.add_policy(
                policy_text=searchable_chunk,
                policy_id=filename,
                metadata={"source": filename, "type": "official_document"}
            )
            print(f"   [+] Indexed {len(text_content)} characters.")
            
        except Exception as e:
            print(f"   [!] Error processing {filename}: {e}")

if __name__ == "__main__":
    ingestor = PolicyIngestor()
    ingestor.ingest_all()