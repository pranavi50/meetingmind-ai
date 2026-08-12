import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai


# Load environment variables
project_folder = Path(__file__).resolve().parent.parent
env_file = project_folder / ".env"
load_dotenv(env_file)

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Create FastAPI application
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
You are an AI meeting assistant.

Analyze the following meeting transcript.

Meeting Title:
{meeting.title}

Transcript:
{meeting.transcript}

Return the result in this exact structure:

Summary:
Write a short summary of the meeting.

Action Items:
List each task and the person responsible for it.

Decisions:
List the important decisions made during the meeting.

Deadlines:
List any deadlines mentioned.

Important Points:
List other important information from the meeting.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {
        "title": meeting.title,
        "analysis": response.text
    }