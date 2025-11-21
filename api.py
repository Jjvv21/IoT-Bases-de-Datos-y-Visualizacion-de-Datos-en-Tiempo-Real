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
        password="root",
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

@app.route("/send-data", methods=["POST"])
def send_data():
    data = request.get_json()

    serial = data.get("serial")

    # Verificación en MySQL
    db = get_mysql()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM dispositivos WHERE serial = %s", (serial,))
    existe = cursor.fetchone()

    if not existe:
        return jsonify({"error": "Dispositivo no registrado"}), 400

    # Insertar lectura en MongoDB
    data["timestamp"] = datetime.utcnow()
    lecturas.insert_one(data)

    return jsonify({"msg": "Lectura recibida", "serial": serial})


# ==========================================
# 4. INICIAR API
# ==========================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
