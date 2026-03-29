import ollama
from core.identity import ARGOS_IDENTITY
from actions.system import get_system_status, handle_action

class ArgosBrain:
    def __init__(self):
        # Asegúrate de que este nombre sea EXACTO al de 'ollama list'
        self.model = "qwen3.5:0.8b" 

    def think(self, message: str) -> str:
        # 1. Comandos directos (CPU, RAM, etc)
        action_result = handle_action(message)
        if action_result: return action_result

        # 2. Status del servidor
        s = get_system_status()
        context = f"SISTEMA: CPU {s['cpu']}% | RAM {s['ram']}% | Temp {s['temp']}."

        try:
            # 3. Llamada ultra-limpia a Ollama
            # Quitamos casi todas las 'options' para dejar que la IA fluya
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': f"{ARGOS_IDENTITY}\nStatus actual: {context}"},
                    {'role': 'user', 'content': message},
                ]
            )

            res = response['message']['content'].strip()

            # 4. Si el modelo devuelve VACÍO, vamos a ver por qué
            if not res:
                # Esto nos dirá si es que el modelo no sabe qué decir
                return f"Rafael, recibo tu señal pero mi núcleo de lenguaje {self.model} no generó respuesta. El sistema está al {s['cpu']}% CPU. Intenta preguntarme algo distinto."

            return res

        except Exception as e:
            return f"Error de conexión con Ollama: {str(e)}"
