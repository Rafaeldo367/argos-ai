import ollama
from core.identity import ARGOS_IDENTITY
from actions.system import get_system_status, handle_action

class ArgosBrain:
    def __init__(self):
        # Asegúrate de que este nombre sea el que te sale en 'ollama list'
        self.model = "qwen3.5:0.8b" 

    def think(self, message: str) -> str:
        # 1. Acciones rápidas (CPU, RAM, Docker)
        action_result = handle_action(message)
        if action_result: 
            return action_result

        # 2. Contexto de servidor (Los 'sentidos' de Argos)
        s = get_system_status()
        context = (
            f"ESTADO DEL SISTEMA:\n- CPU: {s['cpu']}%\n- RAM: {s['ram']}%\n"
            f"- Temp: {s['temp']}\n- Docker: {s['docker']} contenedores\n"
            f"- Uptime: {s['up']}"
        )

        try:
            # 3. Configuración para mayor creatividad
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': f"{ARGOS_IDENTITY}\n\n{context}"},
                    {'role': 'user', 'content': message},
                ],
                options={
                    'temperature': 0.7,    # <--- Sube la creatividad
                    'num_predict': 150,    # <--- Permite respuestas más largas
                    'top_p': 0.9,
                    'stop': ["Usuario:", "User:"]
                }
            )

            res = response['message']['content'].strip()
            
            # Limpieza básica
            res = res.split("Usuario:")[0].strip()

            return res if res else "Estoy procesando datos, Rafael. El flujo es estable."

        except Exception as e:
            return f"Interferencia en el enlace: {str(e)}"
