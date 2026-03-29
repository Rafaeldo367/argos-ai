import ollama
import psutil # Para que Argos tenga "sentidos"
from core.identity import ARGOS_IDENTITY
from actions.system import handle_action

class ArgosBrain:
    def __init__(self):
        self.model = "phi"

    def get_system_context(self):
        """Recolecta datos reales del servidor para darle contexto a Phi."""
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        return f"Contexto del Sistema: CPU: {cpu}%, RAM: {ram}%, Disco: {disk}%."

    def think(self, message: str) -> str:
        # 🔹 1. Intentar acción directa (Prioridad alta)
        action_result = handle_action(message)
        if action_result:
            return action_result

        # 🔹 2. Obtener la realidad del servidor
        context = self.get_system_context()

        # 🔹 3. Construir el prompt estructurado
        # Usamos un formato que Phi entiende mejor para no divagar
        prompt = f"""{ARGOS_IDENTITY}

{context}

Usuario: {message}
Argos:"""

        try:
            # 🔹 4. Llamada optimizada a Ollama
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': 0.2,    # Menos creatividad, más precisión
                    'num_predict': 100,    # Que no escriba testamentos
                    'stop': ["Usuario:", "\n\n"] # Evita que invente diálogos
                }
            )

            # Limpiamos la respuesta de posibles restos
            text = response['response'].strip()
            return text if text else "Sistema en espera. Sin comentarios adicionales."

        except Exception as e:
            return f"Error de cognición local: {str(e)}. Funciones básicas activas."
