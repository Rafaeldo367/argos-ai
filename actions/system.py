import psutil
import subprocess
import os

def get_system_status():
    """Reporte profundo para el contexto de Qwen."""
    # Métricas base
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    # Temperatura (Si el hardware lo permite)
    temp = "N/A"
    try:
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            temp = f"{temps['coretemp'][0].current}°C"
    except: pass

    # Estado de Docker (CasaOS)
    try:
        docker_count = subprocess.check_output(["docker", "ps", "-q"]).decode().count("\n")
    except: docker_count = "Error"

    return {
        "cpu": cpu, "ram": ram, "disk": disk, 
        "temp": temp, "docker": docker_count,
        "up": subprocess.check_output(["uptime", "-p"]).decode().strip()
    }

def handle_action(message: str):
    """Acciones rápidas sin pasar por la IA."""
    msg = message.lower()
    
    if "docker" in msg or "contenedores" in msg:
        try:
            res = subprocess.check_output(["docker", "ps", "--format", "{{.Names}}: {{.Status}}"]).decode()
            return f"Estado Docker:\n{res}"
        except: return "No pude acceder a Docker."

    if "red" in msg or "ip" in msg:
        ip = subprocess.check_output(["hostname", "-I"]).decode().split()[0]
        return f"IP Local: {ip}"

    return None
