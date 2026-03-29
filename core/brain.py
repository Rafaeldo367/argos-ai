import ollama
from core.identity import ARGOS_IDENTITY
from actions.system import get_system_status, handle_action

class ArgosBrain:
    def __init__(self):
        # IMPORTANTE: Cambia esto al nombre exacto de tu 'ollama list'
        # Si descargaste qwen2.5:0.5b o llama3.2:1b, ponlo aquí.
        self.model = "qwen3.5:0.8b" 

    def think(self, message: str) -> str:
        # 1. Acciones rápidas (Si escribes 'CPU', esto responde directo)
        action_result = handle_action(message)
        if action_result: 
            return action_result

        # 2. Contexto simplificado
        s = get_system_status()
        context = f"SISTEMA: CPU {s['cpu']}% | RAM {s['ram']}% | Temp {s['temp']}."

        try:
            # 3. Petición limpia (Sin demasiadas restricciones)
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': f"{ARGOS_IDENTITY}\nStatus: {context}"},
                    {'role': 'user', 'content': message},
                ],
                options={
                    'temperature': 0.8, # Más variedad de palabras
                    'top_p': 0.9,
                    'num_predict': 150, # Permitir que se explaye
                    # Quitamos el stop de salto de línea por si el modelo quiere usar párrafos
                    'stop': ["Usuario:", "User:"] 
                }
            )

            res = response['message']['content'].strip()

            # Si el modelo sigue mudo, forzamos una respuesta basada en datos
            if not res:
                return f"Rafael, el sistema está al {s['cpu']}% de CPU, pero mi núcleo de lenguaje está procesando. ¿Puedes repetir la orden?"

            return res

        except Exception as e:
            return f"Error de enlace: {str(e)}"
