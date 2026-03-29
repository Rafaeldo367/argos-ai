import psutil

def get_system_status():
    """
    Esta función le da a Argos (Phi) la 'visión' del servidor.
    Extrae todos los datos de una vez.
    """
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    # Buscamos procesos que estén consumiendo más del 5%
    heavy_procs = []
    for p in psutil.process_iter(['name', 'cpu_percent']):
        try:
            if p.info['cpu_percent'] > 5.0:
                heavy_procs.append(f"{p.info['name']} ({p.info['cpu_percent']}%)")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
            
    return {
        "cpu": cpu,
        "ram": ram,
        "disk": disk,
        "procs": ", ".join(heavy_procs[:3]) if heavy_procs else "Estable"
    }

def handle_action(message: str):
    """
    Esta función es la 'acción rápida'. 
    Si el usuario pide algo exacto, respondemos sin pasar por la IA.
    """
    message = message.lower()

    if "cpu" in message:
        cpu = psutil.cpu_percent(interval=1)
        return f"Uso actual de CPU: {cpu}%."

    if "ram" in message or "memoria" in message:
        ram = psutil.virtual_memory().percent
        return f"Uso de Memoria RAM: {ram}%."

    if "disco" in message or "disk" in message:
        disk = psutil.disk_usage('/').percent
        return f"Uso de Disco: {disk}%."

    return None
