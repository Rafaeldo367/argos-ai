import os
import psutil

def handle_action(message: str):
    message = message.lower()

    if "cpu" in message:
        cpu = psutil.cpu_percent(interval=1)
        return f"CPU usage is {cpu}%."

    if "ram" in message or "memory" in message:
        ram = psutil.virtual_memory().percent
        return f"Memory usage is {ram}%."

    if "disk" in message:
        disk = psutil.disk_usage('/').percent
        return f"Disk usage is {disk}%."

    return None
