import os
import json
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai


# Load environment variables
project_folder = Path(__file__).resolve().parent.parent
env_file = project_folder / ".env"
load_dotenv(env_file)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)

app = FastAPI(title="MeetingMind AI")


class Meeting(BaseModel):
    title: str
    transcript: str


@app.get("/")
def home():
    return {"message": "MeetingMind AI is running!"}


@app.post("/meetings")
def analyze_meeting(meeting: Meeting):

    prompt = f"""
You are MeetingMind AI, an intelligent meeting analysis assistant.

Analyze this meeting transcript.

Meeting Title:
{meeting.title}

Transcript:
{meeting.transcript}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "summary": "Short summary of the meeting",
    "action_items": [
        {{
            "task": "Task description",
            "owner": "Person responsible"
        }}
    ],
    "decisions": [
        "Important decision made"
    ],
    "deadlines": [
        "Deadline mentioned"
    ],
    "important_points": [
        "Other important information"
    ]
}}

Rules:
- Do not add Markdown.
- Do not add ```json.
- Return only the JSON object.
- If something is not mentioned, return an empty array [].
- Do not invent information.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    try:
        analysis = json.loads(response.text)

    except json.JSONDecodeError:
        return {
            "title": meeting.title,
            "error": "AI returned an invalid JSON response",
            "raw_response": response.text
        }

    return {
        "title": meeting.title,
        "summary": analysis.get("summary", ""),
        "action_items": analysis.get("action_items", []),
        "decisions": analysis.get("decisions", []),
        "deadlines": analysis.get("deadlines", []),
        "important_points": analysis.get("important_points", [])
    }