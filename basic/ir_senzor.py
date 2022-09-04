picocom /dev/tty.usbserial-0001 -b115200


import time
from machine import Pin

ir_sensor = Pin(4, Pin.IN)
onboard_led = Pin(2, Pin.OUT)

while True:
    if not ir_sensor.value():
        onboard_led.off()
    else:
        onboard_led.on()

