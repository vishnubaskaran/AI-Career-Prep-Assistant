import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Read API key
api_key = os.getenv("GEMINI_API_KEY")

print("API Key Found:", api_key is not None)

# Configure Gemini
genai.configure(api_key=api_key)

# Create model
model = genai.GenerativeModel("gemini-2.5-flash")

# Generate response
response = model.generate_content(
    "Give 3 placement interview tips for freshers."
)

print(response.text)