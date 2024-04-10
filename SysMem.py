import psutil
import requests
import time

# Устанавливаем пороговое значение памяти в %
THRESHOLD_PERCENTAGE = 85

# URL для отправки HTTP вебхука
WEBHOOK_URL = 'https://WEBHOOK_URL'

def send_webhook_notification(message):
    data = {'content': message}
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code != 200:
        print(f"Ошибка отправки запроса, код ответа: {response.status_code}")

def monitor_memory_usage():
    while True:
        memory_percentage = psutil.virtual_memory().percent
        if memory_percentage > THRESHOLD_PERCENTAGE:
            message = f"Используется памяти {memory_percentage}%, тригер уведомления использование более {THRESHOLD_PERCENTAGE}%"
            print(memory_percentage)
            send_webhook_notification(message)
        time.sleep(60)  # Проверяем использование памяти каждую минуту

if __name__ == "__main__":
    monitor_memory_usage()
