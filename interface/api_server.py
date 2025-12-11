import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add parent directory to path to find your modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_orchestrator.orchestrator import AIOrchestrator

app = Flask(__name__)
CORS(app)  # Allows your Jekyll site to talk to this Python server

# Initialize the Brain once when the server starts
print(">>> Starting AI Governance Server...")
brain = AIOrchestrator()

@app.route('/api/submit_request', methods=['POST'])
def submit_request():
    """
    Endpoint for the Citizen Interface [Chapter 3.2].
    Receives JSON: { "text": "I need a permit..." }
    Returns JSON: { "decision": ..., "explanation": ... }
    """
    try:
        data = request.json
        user_input = data.get("text", "")
        
        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        print(f"\n[API] Received Request: {user_input[:50]}...")
        
        # Pass the request to your AI Pipeline
        result = brain.process_request(user_input)
        
        return jsonify(result)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "active", "system": "AI-Gov-Framework"})

if __name__ == "__main__":
    # Run on port 5000
    app.run(host='0.0.0.0', port=5001, debug=True)