# 🏛️ AI Policy Orchestrator

**A local-first, multi-agent AI framework for analyzing government policies with privacy guardrails and RAG support.**

  

This project is a **Governance AI System** designed to assist citizens and officials in navigating complex government regulations. It features a microservices architecture that prioritizes **data privacy (PII masking)**, **traceability (RAG citations)**, and **local execution**.

> **Note:** The current version runs in **"Template Mode" (Robot Mode)**. It retrieves accurate documents and performs compliance checks but uses deterministic templates for responses rather than generative LLM synthesis. This ensures 100% predictable output for testing.

-----

## 🚀 Key Features

  * **🔒 Privacy-First Architecture:** Automatically detects and masks PII (names, phone numbers, locations) using **Microsoft Presidio** before any data leaves the client.
  * **🧠 Local RAG (Retrieval-Augmented Generation):** Indexes PDF policies into **ChromaDB** for semantic search without needing cloud APIs.
  * **🕸️ Knowledge Graph Visualization:** visualizes connections between policy keywords using **NetworkX** and **Gephi** formats.
  * **🤖 Multi-Agent Orchestration:**
      * **Orchestrator:** Manages the request flow.
      * **Privacy Guard:** Sanitizes inputs.
      * **Compliance Agent:** Evaluates requests against specific policy constraints (currently logic-based).
  * **💻 Unified Dashboard:** A Jekyll-based frontend providing both a Chat Interface and Interactive Graph Visualizations.

-----

## 🛠️ Tech Stack

### **Backend (Python 3.11)**

  * **Orchestration:** Custom Python Agent Architecture
  * **API:** Flask (REST API)
  * **Vector Database:** ChromaDB (Local persistence)
  * **Privacy/NLP:** Presidio Analyzer, Spacy (`en_core_web_lg`)
  * **Data Processing:** Pandas, PyPDF2, NetworkX

### **Frontend (Static Web)**

  * **Framework:** Jekyll (Ruby)
  * **Styling:** SCSS, CSS Grid
  * **Visualization:** Vis.js (Network Graph)

-----

## 📂 Project Structure

```bash
ai-gov-policy-orchestrator/
├── agent_orchestrator/       # The "Brain" (manages logic flow)
│   └── orchestrator.py       # Main entry point for request handling
├── specialized_agents/       # Domain-specific logic
│   ├── compliance_agent.py   # Checks rules against policies
│   └── extract_keywords.py   # NLP keyword extraction for graphs
├── data_governance/          # Security & Privacy layer
│   └── pii_masking.py        # PII stripping logic
├── knowledge_base/           # RAG & Memory layer
│   ├── vector_store.py       # ChromaDB interface
│   ├── ingest_policies.py    # PDF to Vector ingestor
│   └── retrieve_pdfs.py      # Downloader for policy docs
├── interface/                # Connection layer
│   └── api_server.py         # Flask server connecting Frontend to Backend
├── app/                      # Frontend Source Code
│   ├── index.html            # Main Dashboard & Chat UI
│   └── assets/               # Generated graphs and static files
└── data/                     # Local Storage (Ignored by Git)
    ├── raw_policies/         # Real PDF documents go here
    └── chroma_db/            # Vector database files
```

-----

## ⚡ Getting Started

### Prerequisites

  * **Python 3.11** (Recommended via `pyenv`)
  * **Ruby 3.x** (For Jekyll)
  * **Git**

### 1\. Installation

Clone the repository and set up the Python environment:

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-gov-policy-orchestrator.git
cd ai-gov-policy-orchestrator

# Set up Virtual Environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python Dependencies
pip install -r requirements.txt

# Download Spacy NLP Model (Crucial for PII Masking)
python -m spacy download en_core_web_lg
```

Set up the Frontend (Jekyll):

```bash
# Install Ruby Dependencies
bundle config set --global path '~/.gem'
bundle install
```

### 2\. Data Pipeline Execution

Before running the app, you need to populate the "Brain" with data.

1.  **Mock Data Generation** (Optional, if you don't have scraped data):
    ```bash
    python knowledge_base/mock_scholar_data.py
    ```
2.  **Run the Pipeline**:
    This script downloads PDFs, extracts keywords, and builds the Knowledge Graph.
    ```bash
    ./run_pipeline.sh
    ```
3.  **Ingest Policies**:
    Load the downloaded PDFs into the Vector Database.
    ```bash
    python knowledge_base/ingest_policies.py
    ```

-----

## 🖥️ Running the Application

You need two terminal windows running simultaneously.

**Terminal 1: The Backend (Brain)**
Starts the Flask API on Port 5001.

```bash
python interface/api_server.py
```

**Terminal 2: The Frontend (Face)**
Starts the Jekyll server on Port 4000.

```bash
bundle exec jekyll serve
```

**Access the Dashboard:**
Open your browser to: **[http://127.0.0.1:4000/ai-gov-framework/app/index.html](https://www.google.com/search?q=http://127.0.0.1:4000/ai-gov-framework/app/index.html)**

-----

## 🔮 Future Roadmap

  * [ ] **Full LLM Integration:** Upgrade `orchestrator.py` to support local inference (Ollama/Llama3) or OpenAI GPT-4 for generative answers.
  * [ ] **Live Web Search:** Re-enable SerpApi integration for real-time policy updates.
  * [ ] **Document Upload UI:** Allow users to upload their own PDFs via the dashboard.

-----

## 📄 License

MIT License