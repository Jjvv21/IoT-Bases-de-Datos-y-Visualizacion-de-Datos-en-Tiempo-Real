import pymongo, requests, time
from datetime import datetime, timezone

# Configuración
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "iot_data"
COLL_NAME = "lecturas"
INFLUX_URL = "http://localhost:8081/telegraf"

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
coll = db[COLL_NAME]

last_sent = None

print("Puente MongoDB → InfluxDB iniciado (Ctrl+C para parar)")

while True:
    try:
        query = {}
        if last_sent:
            query = {"timestamp": {"$gt": last_sent}}

        nuevos = list(coll.find(query).sort("timestamp", 1))

        if nuevos:
            for doc in nuevos:
                payload = {
                    "serial": doc["serial"],
                    "voltaje": doc["voltaje"],
                    "corriente": doc["corriente"],
                    "potencia": doc["potencia"]
                }
                requests.post(INFLUX_URL, json=payload, timeout=3)
                last_sent = doc["timestamp"]

            print(f"[{datetime.now().strftime('%H:%M:%S')}] Enviados {len(nuevos)} registros a InfluxDB")

    except Exception as e:
        print("Error:", e)

    time.sleep(7)