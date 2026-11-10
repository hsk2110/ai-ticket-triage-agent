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
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.3)
    )
    return response.text

# 4. Main Automation Pipeline
def process_incoming_tickets(tickets: list):
    logs = []
    urgent_alerts = []

    print("Starting AI Ticket Processing Pipeline...\n")

    for idx, ticket_text in enumerate(tickets, 1):
        print(f"[{idx}/{len(tickets)}] Processing: '{ticket_text[:40]}...")

        # Step A: Classify
        meta = classify_ticket(ticket_text)
        category = meta["category"]
        priority = meta["priority"]
        summary = meta["summary"]

        print(f"   ↳ Category: {category} | Priority: {priority}")

        action_taken = ""

        # Step B: Route logi
        if category in ["SUPPORT", "FEATURE_REQUEST"]:
            draft_text = generate_email_draft(ticket_text, summary)
            draft_filename = f"output/email_drafts/ticket_{idx}_draft.txt"
            with open(draft_filename, "w", encoding="utf-8") as f:
                f.write(f"TO: Customer\nSubject: Re: {summary}\n\n{draft_text}")

            action_taken = f"Created draft ({draft_filename})"

        elif category == "URGENT":
            alert_entry = {
                "ticket_id": idx,
                "timestamp": datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
                "summary": summary,
                "original_message": ticket_text
            }
            urgent_alerts.append(alert_entry)
            action_taken = "ESCALATED: Added to high-priority alert queue"

        elif category == "SPAM":
            action_taken = "IGNORED: Logged as Spam"

        print(f"   ↳ Action: {action_taken}\n")

        # Record for CSV report
        logs.append({
            "id": idx,
            "timestamp": datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
            "category": category,
            "priority": priority,
            "summary": summary,
            "action_taken": action_taken
        })

    # Step C: Save Summary CSV
    csv_path = "output/summary_report.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "timestamp", "category", "priority", "summary", "action_taken"])
        writer.writeheader()
        writer.writerows(logs)
    
    # Step D: Save Urgent Alerts JSON
    if urgent_alerts:
        with open("output/urgent_alerts.json", "w", encoding="utf-8") as f:
            json.dump(urgent_alerts, f, indent=2)

    print(f"Pipeline Execution Finished!")
    print(f"Summary saved to {csv_path}")

if __name__ == "__main__":
    sample_data = [
        "Hi, I forgot my password and the reset link is not working.",
        "URGENT: Our site checkout page is returning 500 server errors!",
        "Cheapest SEO packages guaranteed boost your ranking today!",
        "Could you add an export to PDF feature in the analytics tab?",
        "I need a copy of my tax invoice for September 2026."
    ]
    process_incoming_tickets(sample_data)