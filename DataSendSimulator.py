# send_data.py
from pymongo import MongoClient
from datetime import datetime
import random
import time

# Conexión local
client = MongoClient("mongodb://localhost:27017/") # conexión local
db = client["iot_data"] #nombre de la base de datos
lecturas = db["lecturas"] #nombre de la colección

while True:
    dato = {
        "serial": "ESP32-SIM",
        "voltaje": round(random.uniform(115.0, 125.0), 2),
        "corriente": round(random.uniform(0.2, 0.6), 2),
        "potencia": round(random.uniform(20.0, 60.0), 2),
        "timestamp": datetime.utcnow()
    }
    lecturas.insert_one(dato)
    print("Lectura enviada:", dato)
    time.sleep(5)  # enviar lecturas cada 5 segundos 
