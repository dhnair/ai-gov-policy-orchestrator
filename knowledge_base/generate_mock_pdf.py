from reportlab.pdfgen import canvas
import os

def create_dummy_policy():
    # Ensure the raw policy folder exists
    folder = os.path.join(os.path.dirname(__file__), "../data/raw_policies")
    os.makedirs(folder, exist_ok=True)
    
    file_path = os.path.join(folder, "GO_Housing_Subsidy_2025.pdf")
    
    c = canvas.Canvas(file_path)
    c.drawString(100, 800, "GOVERNMENT ORDER NO. 42/2025 - HOUSING SUBSIDY")
    c.drawString(100, 780, "------------------------------------------------------------")
    c.drawString(100, 750, "SUBJECT: Guidelines for Affordable Housing Assistance")
    
    c.drawString(100, 700, "1. ELIGIBILITY CRITERIA:")
    c.drawString(120, 680, "- The applicant must be a resident of the state for at least 3 years.")
    c.drawString(120, 660, "- Annual family income must be less than $45,000.")
    c.drawString(120, 640, "- Applicant must not own any other residential property.")
    
    c.drawString(100, 600, "2. DOCUMENTATION REQUIRED:")
    c.drawString(120, 580, "- Valid Government ID (Driver's License / Voter ID).")
    c.drawString(120, 560, "- Income Certificate issued by a Gazetted Officer.")
    c.drawString(120, 540, "- Proof of current residence (Utility Bill).")
    
    c.drawString(100, 500, "3. APPLICATION PROCESS:")
    c.drawString(120, 480, "Applications must be submitted via the AI-Gov Portal.")
    
    c.save()
    print(f"✅ Generated Mock Policy: {file_path}")

if __name__ == "__main__":
    create_dummy_policy()
