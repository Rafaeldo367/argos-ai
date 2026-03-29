import os
from dotenv import load_dotenv
from google import genai

from core.identity import ARGOS_IDENTITY
from actions.system import handle_action

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class ArgosBrain:
    def __init__(self):
        pass

    def think(self, message: str) -> str:
        # 1. intentar acción
        action_result = handle_action(message)
        if action_result:
            return action_result

        # 2. pensamiento
        prompt = f"""
{ARGOS_IDENTITY}

User input:
{message}

Argos response:
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash-lite-preview-02-05",
            contents=prompt
        )

        return response.text
