import psutil
import subprocess
import os

def get_system_status():
    """Reporte de sensores para el cerebro de Argos."""
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    # Temperatura
    temp = "N/A"
    try:
        t = psutil.sensors_temperatures()
        if 'coretemp' in t: temp = f"{t['coretemp'][0].current}°C"
        elif 'cpu_thermal' in t: temp = f"{t['cpu_thermal'][0].current}°C"
    except: pass

    # Docker
    try:
        docker_count = subprocess.check_output(["docker", "ps", "-q"]).decode().count("\n")
    except: docker_count = "0 (Error de acceso)"

    return {
        "cpu": cpu, "ram": ram, "disk": disk, 
        "temp": temp, "docker": docker_count,
        "up": subprocess.check_output(["uptime", "-p"]).decode().strip()
    }

def handle_action(message: str):
    """Acciones de control directo."""
    msg = message.lower()
    
    # 1. Ver espacio en disco detallado
    if "espacio" in msg or "disco" in msg:
        res = subprocess.check_output(["df", "-h", "/"]).decode().split('\n')[1]
        parts = res.split()
        return f"Almacenamiento: {parts[2]} usado de {parts[1]} ({parts[4]})."

    # 2. Ver contenedores específicos
    if "docker" in msg or "servicios" in msg:
        try:
            res = subprocess.check_output(["docker", "ps", "--format", "{{.Names}}"]).decode()
            return f"Servicios activos:\n{res}" if res else "No hay contenedores corriendo."
        except: return "Error al consultar Docker."

    # 3. IP y Red
    if "ip" in msg or "red" in msg:
        try:
            ip = subprocess.check_output(["hostname", "-I"]).decode().split()[0]
            return f"Identidad de red: {ip}"
        except: return "No se pudo obtener la IP."

    return None
