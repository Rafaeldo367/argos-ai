import os
import google.generativeai as genai
from dotenv import load_dotenv

from core.identity import ARGOS_IDENTITY
from actions.system import handle_action

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class ArgosBrain:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def think(self, message: str) -> str:
        # primero intenta ejecutar acción
        action_result = handle_action(message)

        if action_result:
            return action_result

        prompt = f"""
{ARGOS_IDENTITY}

User input:
{message}

Argos response:
"""

        response = self.model.generate_content(prompt)
        return response.text
