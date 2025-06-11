import network
import urequests
import time
from machine import ADC, Pin

# --- Configuración Wi-Fi ---
SSID = 'WIFI'
PASSWORD = 'Contraseña'

# --- Configuración sensor HW-481 ---
sensor = ADC(Pin(34))
sensor.atten(ADC.ATTN_11DB)  # Para leer hasta 3.3V
sensor.width(ADC.WIDTH_12BIT)  # Lectura de 0 a 4095

# --- URL del backend Django ---
URL = "http://192.168.1.90:8000/api/api/humedad/"

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a WiFi...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print('Conectado! IP:', wlan.ifconfig()[0])

def enviar_dato(valor):
    porcentaje = int((valor / 4095) * 100)
    headers = {'Content-Type': 'application/json'}
    data = {
        "humedad": valor,
        "porcentaje": porcentaje,
        "sensor_id": "ESP32_1"  # Asegúrate de incluir esto
    }
    try:
        response = urequests.post(URL, json=data)
        print("Status:", response.status_code)
        print("Percenta:", porcentaje)
        response.close()
    except Exception as e:
        print("Error al enviar datos:", e)

# --- Loop principal ---
conectar_wifi()

while True:
    valor_raw = sensor.read()  # valor entre 0 y 4095
    print('Valor humedad (raw):', valor_raw)

    enviar_dato(valor_raw)
    time.sleep(1)
