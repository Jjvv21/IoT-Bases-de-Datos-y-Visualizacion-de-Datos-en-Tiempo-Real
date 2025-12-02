import network
import urequests
import time
import json
import random
import sys
import machine
import math
import urandom


# ============================
# CONFIGURACIÓN DEL DISPOSITIVO
# ============================

SERIAL = "ESP8266-LAB-01"
NOMBRE = "Medidor 1"
TIPO = "Energia"
UBICACION = "Laboratorio A"

API_URL = "http://192.168.1.104:5000"

WIFI_SSID = "Claro - 2.4"
WIFI_PASSWORD = "Apartamento10"


usar_sensores_reales = True


# ============================
# ZMPT101B - VOLTAJE REAL
# ============================

adc = machine.ADC(0)
FACTOR_V = 0.21  # punto de partida, lo podemos ajustar

def leer_voltaje_real(samples=300):
    sq_sum = 0
    for _ in range(samples):
        val = adc.read()
        sq_sum += val * val
        time.sleep_us(200)

    mean = sq_sum / samples
    rms_adc = math.sqrt(mean)
    volt = rms_adc * FACTOR_V
    return round(volt, 2)


def ruido():
    # genera un número entre -1.0 y 1.0
    return (urandom.getrandbits(10) / 512) - 1

# ============================
# CORRIENTE (POR AHORA SIMULADA)
# ============================



def leer_corriente_simulada():
    base = 0.4
    ruido = ((urandom.getrandbits(10) / 512) - 1) * 0.1
    return round(base + ruido, 2)



def obtener_mediciones():
    if usar_sensores_reales:
        voltaje = leer_voltaje_real()
    else:
        voltaje = 120

    corriente = leer_corriente_simulada()    # luego la cambiamos por el SCT real
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




def enviar_datos():
    url = API_URL + "/send-data"

    while True:
        voltaje, corriente, potencia = obtener_mediciones()

        payload = {
            "serial": SERIAL,
            "voltaje": voltaje,
            "corriente": corriente,
            "potencia": potencia
        }

        try:
            r = urequests.post(url, json=payload)
            print("Lectura enviada:", payload)
            r.close()
        except Exception as e:
            print("Error enviando datos:", e)
            conectar_wifi()

        time.sleep(5)


# ============================
# MAIN
# ============================

conectar_wifi()
registrar_dispositivo()
enviar_datos()

