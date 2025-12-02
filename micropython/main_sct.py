import network
import urequests
import time
import math
import machine

# --------------------------
# CONFIGURACIÓN DEL DISPOSITIVO
# --------------------------
SERIAL = "ESP8266-LAB-02"
NOMBRE = "Medidor 2"
TIPO = "Corriente"
UBICACION = "Laboratorio B"

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
# SCT-013 - CORRIENTE REAL
# --------------------------
adc = machine.ADC(0)              # único pin analógico en ESP8266

# Después del divisor 20k+10k, la relación es:
# 1V real en el sensor = 0.333V en el ADC → factor 3
# Sensibilidad del SCT-013-000 = 100 A → 1 V
# Entonces: 100 A → 0.333 V en ADC → 100 A / 0.333 = 300.3
FACTOR_I = 300.3                  # ¡Este es el número mágico para ESP8266 con divisor!

def leer_corriente_rms(muestras=400):
    suma_cuadrados = 0
    for _ in range(muestras):
        valor = adc.read()                 # 0-1023
        voltaje_adc = valor / 1023.0       # 0.0 a 1.0 (aprox)
        voltaje_real = voltaje_adc * 3.0   # porque el divisor multiplica por 3
        voltaje_ac = voltaje_real - 1.65   # quitar offset (Vcc/2)
        suma_cuadrados += voltaje_ac * voltaje_ac
        time.sleep_ms(2)                   # ~500 muestras por segundo

    rms_voltaje = math.sqrt(suma_cuadrados / muestras)
    corriente = rms_voltaje * FACTOR_I
    return round(corriente, 3)

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
        corriente = leer_corriente_rms()
        payload = {
            "serial": SERIAL,
            "corriente": corriente
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


