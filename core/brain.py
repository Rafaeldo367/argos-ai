import ollama
from core.identity import ARGOS_IDENTITY
from actions.system import get_system_status, handle_action

class ArgosBrain:
    def __init__(self):
        # Asegúrate de que el nombre sea exacto al de 'ollama list'
        self.model = "qwen3.5:0.8b" # O el que tengas descargado

    def think(self, message: str) -> str:
        # 1. ¿Es una orden directa? (Acciones de sistema)
        action_result = handle_action(message)
        if action_result: 
            return action_result

        # 2. Contexto de servidor
        s = get_system_status()
        context = (
            f"SISTEMA: CPU {s['cpu']}% | RAM {s['ram']}% | Temp {s['temp']} | "
            f"Docker: {s['docker']} | Uptime: {s['up']}"
        )

        try:
            # 3. Chat optimizado
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': f"{ARGOS_IDENTITY}\nContexto: {context}"},
                    {'role': 'user', 'content': message},
                ],
                options={
                    'temperature': 0.1,    
                    'num_predict': 80,     
                    'top_p': 0.9,          
                    'stop': ["Usuario:", "\n\n", "User:", "Argos:"]
                }
            )

            res = response['message']['content'].strip()
            
            # Limpieza de basura y repeticiones
            res = res.split("Usuario:")[0].split("Argos:")[0].strip()

            # RED DE SEGURIDAD: Evita el error "Message text is empty"
            if not res:
                return "Sistema nominal. Sin novedades que reportar."
            
            return res

        except Exception as e:
            return f"Fallo de enlace neuronal. Error: {str(e)}"
