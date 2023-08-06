import schedule
import threading
import time
import random

def sqs_checker():
    print(">>>>> Checkeando sqs")

    # checkear cola de mensajes
    # simular que aveces se encuentran mensajes y aveces no
    hay_mensajes = random.choice([True, False])
    if hay_mensajes:
        print(f"Mensaje encontrado")
        # comenzar un hilo por procesamiento de mensaje
        process_message(f"message_{round(time.time() * 1000)}")
    else:
        print(">>>>> Ningun mensaje encontrado")

def process_message(message):
    # codigo antes del thread
    # crear thread
    threading.Thread(target=message_processor, daemon=True, args=(message,)).start()

def message_processor(message):
    fake_progress = 0

    # simular progreso de procesamiento del mensaje
    while fake_progress < 100:
        time.sleep(2)
        fake_progress += 10
        print(f"{message} {fake_progress}% procesado")

def main():
    schedule.every(10).seconds.do(sqs_checker)

    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()