import mysql.connector
import datetime


# ----------------------------------------------------
# 1. FUNCIÓN DE CONEXIÓN A MYSQL
# ----------------------------------------------------
def conectar_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1751652",     # <-- cambiar segun cada uno
        database="iot_devices"
    )


# ----------------------------------------------------
# 2. FUNCIÓN PARA REGISTRAR EL DISPOSITIVO
# ----------------------------------------------------
def registrar_dispositivo(serial, nombre="Dispositivo IoT", tipo="Energia", ubicacion="Laboratorio"):
    db = conectar_mysql()
    cursor = db.cursor(dictionary=True)

    # 1️⃣ Verificar si ya existe
    cursor.execute("SELECT * FROM dispositivos WHERE serial = %s", (serial,))
    existe = cursor.fetchone()

    if existe:
        print(f"✔ El dispositivo '{serial}' ya existe en la base.")
        return existe

    # 2️⃣ Insertar un nuevo dispositivo
    insert_sql = """
        INSERT INTO dispositivos (serial, nombre, tipo, ubicacion, estado)
        VALUES (%s, %s, %s, %s, %s)
    """

    valores = (
        serial,
        nombre,
        tipo,
        ubicacion,
        1  # estado: 1 = activo
    )

    cursor.execute(insert_sql, valores)
    db.commit()

    # 3️⃣ Leer el dispositivo recién insertado
    cursor.execute("SELECT * FROM dispositivos WHERE serial = %s", (serial,))
    nuevo = cursor.fetchone()

    print("\n Nuevo dispositivo registrado:")
    print(f"  Serial: {nuevo['serial']}")
    print(f"  Nombre: {nuevo['nombre']}")
    print(f"  Tipo: {nuevo['tipo']}")
    print(f"  Ubicación: {nuevo['ubicacion']}")
    print(f"  Estado: {'Activo' if nuevo['estado'] == 1 else 'Inactivo'}")

    return nuevo



# ----------------------------------------------------
# 3. EJEMPLO DE USO (para pruebas)
# ----------------------------------------------------
if __name__ == "__main__":
    serial_simulado = "ESP8266-SIM-01"
    registrar_dispositivo(serial_simulado)
