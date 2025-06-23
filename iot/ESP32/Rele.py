from machine import Pin
import time

# Configurar el pin GPIO como salida
relay_pin = Pin(5, Pin.OUT)

# Funciones de control
def relay_on():
    relay_pin.on()  # Activar relé

def relay_off():
    relay_pin.off()  # Desactivar relé

print("Abierto")
# Ejemplo de uso
relay_on()   # Enciende el relé
time.sleep(2)  # Espera 2 segundos
relay_off()  # Apaga el relé
print("Cerrado")