import ollama
from core.identity import ARGOS_IDENTITY
from actions.system import get_system_status, handle_action

class ArgosBrain:
    def __init__(self):
        # Asegúrate de que el nombre coincida con 'ollama list'
        self.model = "qwen3.5:0.8b" #El modelo que hayas instalado

    def think(self, message: str) -> str:
        # 1. ¿Es una orden directa?
        action_result = handle_action(message)
        if action_result: return action_result

        # 2. Contexto de servidor
        s = get_system_status()
        context = (
            f"SISTEMA: CPU {s['cpu']}% | RAM {s['ram']}% | Temp {s['temp']} | "
            f"Docker Activos: {s['docker']} | Uptime: {s['up']}"
        )

        try:
            # 3. Chat optimizado para velocidad
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': f"{ARGOS_IDENTITY}\nContexto: {context}"},
                    {'role': 'user', 'content': message},
                ],
                options={
                    'temperature': 0.1,    # Casi sin aleatoriedad (Evita sobrepensar)
                    'num_predict': 60,     # Respuestas cortas = Respuestas rápidas
                    'top_p': 0.9,          # Filtra palabras innecesarias
                    'stop': ["Usuario:", "\n\n", "User:"]
                }
            )

            res = response['message']['content'].strip()
            # Limpiamos si intenta repetir el prompt
            return res.split("Usuario:")[0].split("Argos:")[0].strip()

        except Exception as e:
            return f"Enlace neuronal lento. Error: {str(e)}"
