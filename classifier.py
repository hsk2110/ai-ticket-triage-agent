import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# 2. Initialize Gemini Client
client = genai.Client(api_key=api_key)

# 3. Define the Classification Function
def classify_ticket(message: str) -> dict:
    prompt = f"""
    You are an automated support ticket triage assistant.
    Analyze the following incoming customer message and classify it.

    Incoming Message: "{message}"

    Respond strictly in JSON format with the following key structure:
    {{
        "category": "SUPPORT" | "URGENT" | "SPAM" | "FEATURE_REQUEST",
        "priority": "HIGH" | "MEDIUM" | "LOW",
        "summary": "A 1-sentence summary of the user's issue.",
        "recommended_action": "Suggested next step for automation (e.g. 'draft_email', 'alert_team', 'archive')"
    }}
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1
        )
    )

    return json.loads(response.text)

# 4. Test with sample customer tickets
if __name__ == "__main__":
    test_tickets = [
        "HELP! My production database is down and customers can't log in!",
        "Hi team, where can I find the invoice for my subscription last month?",
        "Buy cheap followers online at ultra low prices click here now!",
        "It would be great if you added dark mode to the dashboard."
    ]

    print("--- Running AI Ticket Classifier Test ---\n")
    for i, ticket in enumerate(test_tickets, 1):
        print(f"Ticket #{i}: '{ticket}'")
        result = classify_ticket(ticket)
        print("Structured Output:", json.dumps(result, indent=2))
        print("-" * 50)