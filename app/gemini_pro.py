import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Client Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_story(outline: list) -> str:
    formatted_outline = "\n".join([
        f"Panel {i+1}: {item.get('title', '')} - {item.get('scene_description', '')}"
        for i, item in enumerate(outline)
    ])
    
    prompt = f"""
You are a comic book writer.

Given the following panel breakdown, write a comic-style story with engaging narration and character dialogues for each panel.

Panel Outline:
{formatted_outline}

Guidelines:
- Use a fun and engaging tone, like an actual comic book.
- Include narration and clearly marked character lines.
- Keep each panel self-contained but part of a cohesive story.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )
    return response.text