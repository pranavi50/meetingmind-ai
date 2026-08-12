import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

project_folder = Path(__file__).resolve().parent.parent
env_file = project_folder / ".env"

load_dotenv(env_file)

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

response = client.responses.create(
    model="gpt-5-mini",
    input="In one sentence, explain what an AI meeting assistant does."
)

print(response.output_text)