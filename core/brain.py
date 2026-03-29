import ollama
from core.identity import ARGOS_IDENTITY
from actions.system import get_system_status, handle_action

class ArgosBrain:
    def __init__(self):
        self.model = "phi"

    def think(self, message: str) -> str:
        # 1. Acción directa (psutil, etc)
        action_result = handle_action(message)
        if action_result:
            return action_result

        # 2. Obtener la realidad del servidor
        status = get_system_status()
        context = (
            f"DATOS DEL SISTEMA: CPU {status['cpu']}%, "
            f"RAM {status['ram']}%, DISCO {status['disk']}%.\n"
            f"PROCESOS: {status['procs']}."
        )

        try:
            # 3. Usar la API de Chat (Más robusta)
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': f"{ARGOS_IDENTITY}\n\n{context}"},
                    {'role': 'user', 'content': message},
                ],
                options={
                    'temperature': 0.1,  # Máxima precisión, mínima "locura"
                    'stop': ["User:", "Usuario:", "\n\n", "AI:", "Argos:"], # MORDaza
                    'num_predict': 80    # Que sea breve y directo
                }
            )

            # Limpiamos cualquier residuo que Phi haya intentado colar
            full_response = response['message']['content'].strip()
            
            # Si se pone a traducir entre paréntesis, cortamos eso
            clean_response = full_response.split('(')[0].strip()
            
            return clean_response if clean_response else "Sistema operativo. Sin novedades."

        except Exception as e:
            return f"Fallo de cognición: {str(e)}"
