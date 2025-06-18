from machine import Pin, Timer
import time
import dht
import network
import urequests

Sensor_Flujo = Pin(15, Pin.IN)
Sensor_HumedadTemperatura = dht.DHT11(Pin(14))

# Variable para contar pulsos
pulses = 0

# Calibración: cada pulso es aproximadamente 0.0075 litros
litros_por_pulso = 0.0075

# --- Configuración Wi-Fi ---
SSID = 'Dpto 601'
PASSWORD = '94434657'

# --- URL del backend Django ---
URL = "http://192.168.1.93:8000/api/datos/"

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a WiFi...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print('Conectado! IP:', wlan.ifconfig()[0])

# Interrupción para contar pulsos
def count_pulses(pin):
    global pulses
    pulses += 1

# Temporizador para calcular el flujo
timer = Timer(0)

def calcular_flujo():
    global pulses
    flujo = pulses * litros_por_pulso  # Calcular el flujo en litros
    pulses = 0  # Reiniciar el contador de pulsos
    return flujo

# Función principal para medir flujo
def medir_flujo():
    global timer
    # Configuración de la interrupción
    Sensor_Flujo.irq(trigger=Pin.IRQ_RISING, handler=count_pulses)

    # Configuración del temporizador para calcular flujo cada segundo
    timer.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: calcular_flujo())
    
    try:
        # Medir flujo indefinidamente
        while True:
            flujo = calcular_flujo()
            print("Flujo: {:.2f} L/s".format(flujo))
            time.sleep(1)
            return flujo  # Retorna el flujo calculado
    except KeyboardInterrupt:
        print("Error midiendo flujo.")
        timer.deinit()  # Detener el temporizador al finalizar

def medir_humedad_temperatura():
      try:
        time.sleep(0.5)
        Sensor_HumedadTemperatura.measure()
        temp = Sensor_HumedadTemperatura.temperature()
        hum = Sensor_HumedadTemperatura.humidity()
        print('Temperature: %3.1f C' %temp)
        print('Humidity: %3.1f %%' %hum)
        print("")
        
        return (temp, hum)
      except OSError as e:
        print('Failed to read sensor.')

def enviar_datos(humedad, temperatura, flujo):
    headers = {'Content-Type': 'application/json'}
    data = {
        "humedad": humedad,
        "temperatura": temperatura,
        "flujo": flujo,
        "sensor_id": "ESP32_1"  # Asegúrate de incluir esto
    }
    try:
        response = urequests.post(URL, json=data)
        print("Status:", response.status_code)
        response.close()
    except Exception as e:
        print("Error al enviar datos:", e)


def main():
    conectar_wifi()
    
    while True:
        flujo = medir_flujo()
        temperatura, humedad = medir_humedad_temperatura()
        print(f"h: {humedad} t: {temperatura} f: {flujo}")
        enviar_datos(humedad, temperatura, flujo)
        print()
        
        

main()