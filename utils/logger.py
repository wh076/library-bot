import os
from datetime import datetime

LOGS_DIR = "logs"

# Автоматически создаем папку для логов, если её нет
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

def log_user_action(user_id: int, request: str, action: str, result: str):
    """
    Записывает всю историю взаимодействия пользователя с программой.
    Формат файла: logs/{ID}.log
    """
    filename = os.path.join(LOGS_DIR, f"{user_id}.log")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = (
        f"[{timestamp}]\n"
        f"User Request: {request}\n"
        f"Action Performed: {action}\n"
        f"Result/Response: {result}\n"
        f"{'-'*40}\n"
    )
    
    with open(filename, "a", encoding="utf-8") as file:
        file.write(log_entry)