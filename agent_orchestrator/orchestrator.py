import sys
import json
import datetime
from specialized_agents.compliance_agent import ComplianceAgent

# Add parent directory to path so we can import our other modules
sys.path.append(".")

from data_governance.pii_masking import PIIMasker
from knowledge_base.vector_store import PolicyKnowledgeBase

class AIOrchestrator:
    """
    The 'Brain' of the system [Chapter 4.1].
    Coordinates: User Input -> PII Masking -> Intent Classification -> RAG Search -> Final Answer.
    """
    def __init__(self):
        print(">>> Initializing AI Gov Orchestrator...")
        
        # 1. Initialize the Guardrails (Privacy)
        self.privacy_guard = PIIMasker()
        
        # 2. Initialize the Memory (RAG)
        self.knowledge_base = PolicyKnowledgeBase()
        
        # 3. Log the startup
        self.session_id = str(datetime.datetime.now().timestamp())

        # 4. Initialize the Compliance Agent
        self.compliance_agent = ComplianceAgent()

    def process_request(self, user_input):
        """
        Main pipeline logic.
        """
        print(f"\n--- Processing Request: {self.session_id} ---")

        # Step A: PII Masking (Safety First)
        # We don't want to send real names/phones to the LLM or logs
        clean_text = self.privacy_guard.mask_text(user_input)
        print(f"[Privacy] Masked Input: {clean_text}")

        # Step B: Policy Retrieval (RAG)
        # Use the masked text to find relevant laws
        print("[RAG] Searching for relevant policies...")
        relevant_policies = self.knowledge_base.query_policy(clean_text)
        
        # Extract the text from the search results
        context_docs = relevant_policies['documents'][0] if relevant_policies['documents'] else []
        
        print(f"[RAG] Found {len(context_docs)} relevant policy documents.")

        # Step C: Delegate to Compliance Agent
        # The Orchestrator shouldn't guess; it asks the expert.
        print("[Orchestrator] Delegating to Compliance Agent...")
        
        agent_decision = self.compliance_agent.evaluate(
            request_text=clean_text,
            policy_context=context_docs
        )
        
        return {
            "original_input": user_input,
            "masked_input": clean_text,
            "policies_used": context_docs,
            "expert_decision": agent_decision
        }

    def generate_llm_response(self, user_query, context):
        """
        MOCK LLM INTERFACE.
        For now, returns a logic-based response so you can run it offline without API keys.
        """
        if not context:
            return "I could not find any specific government policies related to your query."
        
        # Simple template-based response
        return (
            f"Based on the following policies: '{context[0]}', "
            f"I can advise that your request regarding '{user_query}' requires "
            "compliance with the stated income or documentation limits."
        )

# --- Self-Test Block ---
if __name__ == "__main__":
    # This allows you to run the orchestrator directly to test it
    orchestrator = AIOrchestrator()
    
    # Simulate a user
    user_msg = "My name is Deepak, phone 9876543210. I want to apply for a housing subsidy."
    
    result = orchestrator.process_request(user_msg)
    
    print("\n>>> FINAL OUTPUT:")
    print(json.dumps(result, indent=2))