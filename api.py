from flask import Flask, request, jsonify
import mysql.connector
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)


# ==========================================
# 1. CONEXIONES A LAS BASES DE DATOS
# ==========================================

def get_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",

        password="1751652",

        database="iot_devices"
    )


mongo = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo["iot_data"]
lecturas = mongo_db["lecturas"]


# ==========================================
# 2. ENDPOINT PARA REGISTRAR DISPOSITIVO
# ==========================================

@app.route("/register-device", methods=["POST"])
def register_device():
    data = request.get_json()

    serial = data.get("serial")
    nombre = data.get("nombre")
    tipo = data.get("tipo")
    ubicacion = data.get("ubicacion")

    db = get_mysql()
    cursor = db.cursor(dictionary=True)

    # Verificar si ya existe
    cursor.execute("SELECT * FROM dispositivos WHERE serial = %s", (serial,))
    existe = cursor.fetchone()

    if existe:
        return jsonify({"msg": "Dispositivo ya existía", "serial": serial}), 200

    # Insertar nuevo
    insert_sql = """
    INSERT INTO dispositivos (serial, nombre, tipo, ubicacion, estado)
    VALUES (%s, %s, %s, %s, 1)
    """

    cursor.execute(insert_sql, (serial, nombre, tipo, ubicacion))
    db.commit()

    return jsonify({"msg": "Dispositivo registrado con éxito", "serial": serial})


# ==========================================
# 3. ENDPOINT PARA RECIBIR LECTURAS
# ==========================================

# Variables globales para combinar lecturas
ultimo_voltaje = None
ultima_corriente = None

@app.route("/send-data", methods=["POST"])
def recibir_datos():
    global ultimo_voltaje, ultima_corriente

    data = request.get_json()

    serial = data.get("serial")
    voltaje = data.get("voltaje")
    corriente = data.get("corriente")

    timestamp = datetime.now()

    # Guardamos lecturas por separado
    if voltaje is not None:
        ultimo_voltaje = voltaje

    if corriente is not None:
        ultima_corriente = corriente

    # Cálculo de potencia real (solo si ambos existen)
    potencia = None
    if ultimo_voltaje is not None and ultima_corriente is not None:
        potencia = round(ultimo_voltaje * ultima_corriente, 3)

    # Guardar en MongoDB
    lecturas.insert_one({
        "serial": serial,
        "voltaje": voltaje,
        "corriente": corriente,
        "potencia": potencia,
        "timestamp": timestamp
    })

    print("Lectura guardada:", data, "Potencia:", potencia)

    return jsonify({
        "msg": "OK",
        "serial": serial,
        "voltaje": voltaje,
        "corriente": corriente,
        "potencia": potencia,
        "timestamp": str(timestamp)
    })


# ==========================================
# 4. INICIAR API
# ==========================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
