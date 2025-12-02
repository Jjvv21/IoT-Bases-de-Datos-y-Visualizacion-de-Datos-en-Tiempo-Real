import network
import urequests
import time
import math
import machine

# --------------------------
# CONFIGURACIÓN DEL DISPOSITIVO
# --------------------------
SERIAL = "ESP8266-LAB-01"
NOMBRE = "Medidor 1"
TIPO = "Energia"
UBICACION = "Laboratorio A"

API_URL = "http://192.168.1.104:5000"

WIFI_SSID = "Claro - 2.4"
WIFI_PASSWORD = "Apartamento10"


# --------------------------
# WIFI
# --------------------------
def conectar_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)

    if not wifi.isconnected():
        print("Conectando al WiFi...")
        wifi.connect(WIFI_SSID, WIFI_PASSWORD)

        while not wifi.isconnected():
            time.sleep(0.5)

    print("WiFi conectado:", wifi.ifconfig())


# --------------------------
# ZMPT101B - VOLTAJE REAL
# --------------------------
import machine
import math
import time

# Configuración ADC
adc = machine.ADC(0)  # A0 del ESP8266
FACTOR_V = 0.21  # Ajustarás después con calibración real


# --- CALIBRAR OFFSET (hacer UNA VEZ con el sensor DESCONECTADO de 110V) ---
def calibrar_offset(muestras=1000):
    suma = 0
    for _ in range(muestras):
        suma += adc.read()
        time.sleep(0.001)
    offset = suma / muestras
    print(f"Offset calibrado: {offset:.2f} (ADC units)")
    return offset


# Llama esta función con el sensor DESCONECTADO de la red
OFFSET = calibrar_offset()  # Ej: te dará ~512 si está en 2.5V


# Guarda este valor y úsalo en la función principal

# --------------------------
# ZMPT101B - VOLTAJE RMS CORRECTO
# --------------------------
def leer_voltaje_rms():
    muestras = 100
    suma_cuadrados = 0

    for _ in range(muestras):
        lectura = adc.read()
        voltaje_centrado = lectura - OFFSET  # ¡¡RESTAMOS EL OFFSET!!
        suma_cuadrados += voltaje_centrado * voltaje_centrado
        time.sleep(0.001)  # ~1ms → 1000 muestras/seg → cubre varios ciclos de 60Hz

    # RMS del valor centrado
    rms_adc = math.sqrt(suma_cuadrados / muestras)

    # Convertir a voltaje real (RMS)
    voltaje_rms = rms_adc * FACTOR_V
    return round(voltaje_rms, 2)


# --------------------------
# API
# --------------------------
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
        volt = leer_voltaje_rms()
        payload = {
            "serial": SERIAL,
            "voltaje": volt
        }
        try:
            r = urequests.post(url, json=payload)
            print("Enviado:", payload)
            r.close()
        except Exception as e:
            print("Error:", e)
            conectar_wifi()
        time.sleep(5)


# --------------------------
# MAIN
# --------------------------
conectar_wifi()
registrar_dispositivo()
enviar_datos()
calibrar_offset()

