from google import genai
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_json(text: str):
    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
    if not match:
        raise ValueError("Invalid LLM response")

    parsed = json.loads(match.group(1))

    if isinstance(parsed, dict) and "tasks" in parsed:
        return parsed["tasks"]

    if isinstance(parsed, list):
        return parsed

    raise ValueError("Invalid task format")


def generate_tasks(transcript: str):
    prompt = f"""
You are a backend system.

Return ONLY valid JSON.
No markdown. No explanations.

The response MUST be a JSON array.

Each task must contain:
- id
- description
- priority (low | medium | high)
- dependencies (array of ids)

Transcript:
{transcript}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return extract_json(response.text)
