import sys
# Ensure we can import modules from the parent directory if needed
sys.path.append("..")

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

class PIIMasker:
    """
    Implements the 'Privacy Enhancing Technologies (PETs)' requirement [Chapter 6.2].
    Detects and masks names, phones, and locations to ensure GDPR/CPRA compliance.
    """
    def __init__(self):
        # Initialize the NLP engines (using Spacy under the hood)
        print(">>> Initializing PII Governance Module...")
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    def mask_text(self, text):
        """
        Scans text for sensitive info and replaces it with generic tags.
        Input: "My name is Deepak."
        Output: "My name is <PERSON>."
        """
        if not text:
            return ""

        # 1. Analyze: Find the PII entities
        results = self.analyzer.analyze(
            text=text,
            language='en',
            entities=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "LOCATION", "US_DRIVER_LICENSE"]
        )

        # 2. Anonymize: Replace PII with generic tags
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results
        )
        
        return anonymized_result.text

# --- Self-Test Block ---
if __name__ == "__main__":
    masker = PIIMasker()
    
    # Simulate a citizen submission
    test_input = "My name is Deepak Nair, living in Bangalore. Contact me at 9876543210."
    
    masked_output = masker.mask_text(test_input)
    
    print("-" * 40)
    print(f"Original: {test_input}")
    print(f"Masked:   {masked_output}")
    print("-" * 40)