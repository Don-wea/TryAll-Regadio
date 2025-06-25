import network
import urequests
import ujson
import time
from machine import Pin, Timer

sensor_pin = Pin(15, Pin.IN)

# Configuración de WiFi
SSID = 'Dpto 601'  # Reemplazar con tu SSID
PASSWORD = '94434657'  # Reemplazar con tu contraseña

# URL del backend
URL = 'http://192.168.1.87:8000'
BASE_URL_OBTENER = f'{URL}/api/recibir_flujo/'  # URL para obtener cantidad_flujo
BASE_URL_POST = f'{URL}/api/enviar_flujo/'  # URL para actualizar cantidad_flujo
BASE_URL_ENVIAR_FLUJO_ACTUAL = f'{URL}/api/enviar_flujo_actual/'

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print('Conectando a WiFi...')
        wlan.connect(SSID, PASSWORD)

        # Esperar a que se conecte
        timeout = 10  # Timeout de 10 segundos
        start_time = time.ticks_ms()
        while not wlan.isconnected():
            if time.ticks_ms() - start_time > timeout * 1000:
                print("❌ Conexión WiFi fallida")
                return False
            time.sleep(1)

    print('Conectado! IP:', wlan.ifconfig()[0])
    return True

def obtener_flujo():
    try:
        response = urequests.get(BASE_URL_OBTENER)
        print("Código de respuesta:", response.status_code)
        
        # Parsear el JSON
        data = ujson.loads(response.text)
        cantidad_flujo = data.get("cantidad_flujo")  # Extraer el valor de cantidad_flujo
        
        print("Cantidad de flujo objetivo:", cantidad_flujo)
        
        
        response.close()  # Cerrar la respuesta para liberar memoria
        return cantidad_flujo  # Retornar el valor para usarlo en el programa
    except Exception as e:
        print("Error en la solicitud GET:", e)
        return None

def enviar_flujo_a_cero():
    try:
        # Construir la URL con el parámetro de consulta
        url_completa = f'{BASE_URL_POST}?cantidad_flujo=0'
        
        response = urequests.post(url_completa)  # Usar GET en lugar de POST
        print("Código de respuesta:", response.status_code)

        if response.status_code == 200:
            print("Cantidad de flujo actualizada a 0 exitosamente.")
        else:
            print("Error al actualizar cantidad de flujo:", response.text)

        response.close()  # Cerrar respuesta para liberar memoria
    except Exception as e:
        print("Error en la solicitud:", e)


    
flujo_actual = 0
flujo_total = 0


def enviar_flujo_actual():
    global flujo_actual
    try:
        URL_COMPLETA = f'{BASE_URL_ENVIAR_FLUJO_ACTUAL}?flujo_actual={flujo_actual}'
        
        response = urequests.post(URL_COMPLETA)
        
        if response.status_code == 200:
            print(f'Flujo actual actualizado a {flujo_actual} exitosamente.')
        else:
            print("Error al actualizar cantidad de flujo:", response.text)
    
        response.close()
    
    except Exception as e:
        print("Error en la solicitud:", e)  

pulses = 0

def count_pulses(pin):
    global pulses
    pulses += 1
    
sensor_pin.irq(trigger=Pin.IRQ_RISING, handler=count_pulses)

litros_por_pulso = 0.0075

def print_flujo(timer):
    global pulses
    global flujo_actual
    global flujo_total
    
    flujo_actual = pulses * litros_por_pulso
    flujo_total = flujo_total + flujo_actual
    
    print("Flujo: {:.2f} L/s".format(flujo_actual))
    print("FLUJO: ", flujo_actual)
    print()
    print("Flujo total: {:.2f} L".format(flujo_total))
    print("FLUJO TOTAL: ", flujo_total)
    pulses = 0
    

rele_pin = Pin(5, Pin.OUT)

def rele_riego_on():
    rele_pin.on()
    
def rele_riego_off():
    rele_pin.off()
    


def regar(flujo_objetivo):
    global flujo_total
    
    timer = Timer(0)
    timer.init(period=1000, mode=Timer.PERIODIC, callback=print_flujo)
    

    rele_riego_on()
    
    while flujo_total < flujo_objetivo:
        flujo_objetivo = obtener_flujo()
        print(f"Regando. Flujo total: {flujo_total}. Flujo objetivo: {flujo_objetivo}")
    
    print("RIEGO TERMINADO")
    
    rele_riego_off()
    flujo_total = 0
    enviar_flujo_a_cero()  # Enviar POST para cambiar cantidad_flujo a 0





def main():
    print("Iniciando la prueba de conexión y solicitud GET")
    if conectar_wifi():
        while True:
            cantidad_flujo = obtener_flujo()
            enviar_flujo_actual()
            if cantidad_flujo > 0:
                print("Iniciando riego")
                regar(cantidad_flujo)

# Ejecutar el programa principal
if __name__ == '__main__':
    main()
