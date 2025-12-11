import os
import chromadb
from chromadb.utils import embedding_functions

class PolicyKnowledgeBase:
    """
    Implements the Vector Database for Retrieval-Augmented Generation (RAG).
    Stores policy documents as 'embeddings' for semantic search [Chapter 5.1].
    """
    def __init__(self, db_path="./data/chroma_db"):
        # Ensure the data directory exists
        os.makedirs(db_path, exist_ok=True)
        
        # Initialize a persistent client (saves data to disk)
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Use a lightweight CPU-friendly embedding model (MiniLM)
        # This converts text into numbers locally (No GPU needed)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2" 
        )
        
        # Create or get the collection (think of it as a 'table' of policies)
        self.collection = self.client.get_or_create_collection(
            name="gov_policies",
            embedding_function=self.embedding_fn
        )
        print(f">>> Knowledge Base loaded from {db_path}")

    def add_policy(self, policy_text, policy_id, metadata):
        """
        Ingests a policy document into the vector database.
        """
        print(f"Indexing Policy: {policy_id}")
        self.collection.upsert(
            documents=[policy_text],
            metadatas=[metadata],
            ids=[policy_id]
        )

    def query_policy(self, query_text, n_results=2):
        """
        Finds the most relevant policies for a user's question.
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results

# --- Self-Test Block ---
if __name__ == "__main__":
    kb = PolicyKnowledgeBase()
    
    # 1. Add some sample 'Government Policies' (Simulating Chapter 6.1 Data Sources)
    kb.add_policy(
        policy_text="Citizens are eligible for housing subsidies if their annual income is below $30,000.",
        policy_id="housing_act_sec_4",
        metadata={"category": "housing", "source": "Housing Act 2024"}
    )
    
    # 2. Simulate a user asking a question
    user_query = "How do I get financial help for a house?"
    matches = kb.query_policy(user_query)
    
    print("-" * 40)
    print(f"Query: {user_query}")
    print(f"Retrieved Policy: {matches['documents'][0][0]}")
    print("-" * 40)