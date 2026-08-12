import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

project_folder = Path(__file__).resolve().parent.parent
env_file = project_folder / ".env"

load_dotenv(env_file)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Gemini API key not found!")
    exit()

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="In one sentence, explain what an AI meeting assistant does."
)

print(response.text)