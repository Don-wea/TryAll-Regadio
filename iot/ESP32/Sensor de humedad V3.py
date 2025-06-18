from machine import Pin
from time import sleep
import dht 

sensor = dht.DHT11(Pin(14))
#sensor = dht.DHT11(Pin(14))

while True:
  try:
    sleep(0.5)
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    temp_f = temp * (9/5) + 32.0
    print('Temperature: %3.1f C' %temp)
    print('Humidity: %3.1f %%' %hum)
    print("")
  except OSError as e:
    print('Failed to read sensor.')