import os
import json
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_outline(user_prompt: str) -> list:
    prompt = f"""
You are a professional AI comic planner.

Your task is to generate a strictly formatted JSON array containing 5 panel descriptions for a comic based on the story idea below:

STORY: "{user_prompt}"

Each JSON object must include:
- "panel" (integer)
- "title" (string)
- "scene_description" (string)
- "image_prompt" (string)

Respond ONLY in this valid JSON format, without any explanations or markdown:
[
  {{
    "panel": 1,
    "title": "Sample Title",
    "scene_description": "Sample Description",
    "image_prompt": "Sample Prompt"
  }}
]
"""

    for attempt in range(4):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )
            break
        except Exception as e:
            if attempt < 3:
                time.sleep(3)
                continue
            raise e

    raw_text = response.text.strip()
    if raw_text.startswith("json"):
        raw_text = raw_text.replace("json", "").replace("", "").strip()
    elif raw_text.startswith(""):
        raw_text = raw_text.replace("```", "").strip()

    return json.loads(raw_text)