from machine import Pin, Timer
import time

# Configuración del pin para el sensor
sensor_pin = Pin(15, Pin.IN)

# Variable para contar pulsos
pulses = 0

# Interrupción para contar pulsos
def count_pulses(pin):
    global pulses
    pulses += 1

# Configuración de la interrupción
sensor_pin.irq(trigger=Pin.IRQ_RISING, handler=count_pulses)

# Calibración: cada pulso es aproximadamente 0.0075 litros
litros_por_pulso = 0.0075

# Timer para imprimir los datos cada segundo
def print_flow(timer):
    global pulses
    flujo = pulses * litros_por_pulso  # Calcular el flujo en litros
    print("Flujo: {:.2f} L/s".format(flujo))
    pulses = 0  # Reiniciar el contador de pulsos

# Configuración del temporizador
timer = Timer(0)
timer.init(period=1000, mode=Timer.PERIODIC, callback=print_flow)

# Bucle principal
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Programa terminado.")