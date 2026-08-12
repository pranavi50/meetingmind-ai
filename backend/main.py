from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Meeting(BaseModel):
    title: str
    transcript: str


@app.get("/")
def home():
    return {"message": "MeetingMind AI is running!"}


@app.post("/meetings")
def create_meeting(meeting: Meeting):
    return {
        "message": "Meeting received successfully!",
        "title": meeting.title,
        "transcript": meeting.transcript
    }