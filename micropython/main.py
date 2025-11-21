import network
import urequests
import time
import json
import random

# ============================
# CONFIGURACIÓN DEL DISPOSITIVO
# ============================

SERIAL = "ESP8266-LAB-01"
NOMBRE = "Medidor 1"
TIPO = "Energia"
UBICACION = "Laboratorio A"

API_URL = "http://TU_IP_O_DOMINIO:5000"   # <---- Cambiar cuando tengas la API corriendo

WIFI_SSID = "nombreRed"
WIFI_PASSWORD = "contrasena"


usar_sensores_reales = False


# ============================
# FUNCIONES DE SENSORES
# ============================

# --- Simulación de sensores --- #
def leer_voltaje_simulado():
    base = 120  # voltaje típico
    ruido = random.uniform(-5, 5)
    return round(base + ruido, 2)


def leer_corriente_simulada():
    base = 0.45  # amperaje típico
    ruido = random.uniform(-0.15, 0.15)
    return round(base + ruido, 2)


# --- Sensores reales (cuando los tengas) --- #
def leer_voltaje_real():
    # Aquí irá el código del ZMPT101B o ADC
    # Ejemplo:
    # val = adc.read()
    # volt = convertir_a_voltaje(val)
    # return volt
    return leer_voltaje_simulado()  # por ahora simulado


def leer_corriente_real():
    # Aquí irá la lectura del SCT-013
    # Ejemplo:
    # corriente = calcular_corriente(transformer.read())
    return leer_corriente_simulada()  # por ahora simulado


# Función principal de lectura:
def obtener_mediciones():
    if usar_sensores_reales:
        voltaje = leer_voltaje_real()
        corriente = leer_corriente_real()
    else:
        voltaje = leer_voltaje_simulado()
        corriente = leer_corriente_simulada()

    potencia = round(voltaje * corriente, 2)

    return voltaje, corriente, potencia

# ============================
# 1. CONECTARSE AL WIFI
# ============================

def conectar_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)

    if not wifi.isconnected():
        print("Conectando al WiFi...")
        wifi.connect(WIFI_SSID, WIFI_PASSWORD)

        while not wifi.isconnected():
            time.sleep(0.5)

    print("WiFi conectado:", wifi.ifconfig())


# ============================
# 2. REGISTRAR DISPOSITIVO EN PYTHON
# ============================

def registrar_dispositivo():
    url = API_URL + "/register-device"

    payload = {
        "serial": SERIAL,
        "nombre": NOMBRE,
        "tipo": TIPO,
        "ubicacion": UBICACION
    }

    try:
        r = urequests.post(url, json=payload)
        print("Respuesta registro:", r.text)
        r.close()
    except Exception as e:
        print("Error registrando:", e)


# ============================
# 3. ENVIAR DATOS SIMULADOS
# ============================

def enviar_datos():
    url = API_URL + "/send-data"

    while True:
        payload = {
            "serial": SERIAL,
            "voltaje": 115 + 5,  # puedes cambiar esto luego
            "corriente": 0.4,
            "potencia": 52.3
        }

        try:
            r = urequests.post(url, json=payload)
            print("Lectura enviada:", r.text)
            r.close()
        except Exception as e:
            print("Error enviando datos:", e)

        time.sleep(5)


# ============================
# PROGRAMA PRINCIPAL
# ============================

conectar_wifi()
registrar_dispositivo()
enviar_datos()
