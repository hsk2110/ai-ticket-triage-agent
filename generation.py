import os
import json
import csv
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Setup & Initialization
load_dotenv()
# Get and verify the key exists
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found")
# Initialize the Gemini client
client = genai.Client(api_key=api_key)

# make the email draft directory
os.makedirs("output/email_drafts", exist_ok=True)

# 2. Classifier function
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

# 3. Email response generator
def generate_email_draft(customer_message: str, summary: str) -> str:
    prompt = f"""
    You are a polite, helpful customer support representative.
    Write a clear, professional email reply addressing the customer's issue.

    Customer Issue Summary: {summary}
    Original Message: "{customer_message}"

    Keep the response concise (2-3 paragraphs max) and empathetic.
    """
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.3)
    )
    return response.text


if __name__ == "__main__":
    sample_data = [
        "Hi, I forgot my password and the reset link is not working.",
        "URGENT: Our site checkout page is returning 500 server errors!",
        "Cheapest SEO packages guaranteed boost your ranking today!",
        "Could you add an export to PDF feature in the analytics tab?",
        "I need a copy of my tax invoice for September 2026."
    ]

    for msg in sample_data:
        res = classify_ticket(msg)
        print(f"Processed: {res['category']} | {res['priority']}")