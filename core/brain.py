import subprocess
from core.identity import ARGOS_IDENTITY
from actions.system import handle_action

class ArgosBrain:
    def __init__(self):
        pass

    def think(self, message: str) -> str:
        # 🔹 1. intentar acción directa
        action_result = handle_action(message)
        if action_result:
            return action_result

        # 🔹 2. pensamiento con modelo local (Phi)
        prompt = f"""
{ARGOS_IDENTITY}

User:
{message}

Argos:
"""

        try:
            result = subprocess.run(
                ["ollama", "run", "phi"],
                input=prompt,
                text=True,
                capture_output=True
            )

            return result.stdout.strip()

        except Exception:
            return "Local cognition unavailable. System functions remain active."
