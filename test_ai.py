import os
from dotenv import load_dotenv
from google import genai

# load environment variables from .env
load_dotenv()

# Get and verify the key exists
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

# Initialize the Gemini client
client = genai.Client(api_key=api_key)

print("Sending request to Gemini...")

# Request a reponse from gemini-3.5-flash-lite
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Briefly explain what an AI Automation Agent does in 2 sentences."
)

print("\n--- AI Response ---")
print(response.text)