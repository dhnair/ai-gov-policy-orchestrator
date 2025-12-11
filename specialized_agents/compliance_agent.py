import json

class ComplianceAgent:
    """
    The 'Expert' that evaluates if a request meets regulations [Chapter 4.1].
    """
    def __init__(self):
        print(">>> Compliance Agent Activated.")

    def evaluate(self, request_text, policy_context):
        """
        Compares the User's Request vs. The Official Policy.
        Returns a structured decision.
        """
        print(f"   [ComplianceAgent] Evaluating request against {len(policy_context)} policies...")
        
        # MOCK LLM LOGIC (Replace with real LLM API call in production)
        # Logic: If we found a policy, we assume we need to check it.
        
        if not policy_context:
            return {
                "status": "UNCERTAIN",
                "reason": "No relevant policies found in the database.",
                "confidence": 0.1
            }

        # Simulated Logic: Check if the policy mentions "income" or "eligible"
        main_policy = policy_context[0]
        
        decision = {
            "status": "PENDING_REVIEW", # Default to safety
            "reason": f"Evaluated against policy: {main_policy[:100]}...",
            "confidence": 0.85,
            "next_step": "Human Verification Required"
        }
        
        return decision