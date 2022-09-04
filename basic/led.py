picocom /dev/tty.usbserial-0001 -b115200


import time
from machine import Pin

onboard_led = Pin(2, Pin.OUT)
onboard_led.off() 
onboard_led.on()

while True:
    time.sleep(0.5)
    onboard_led.off() 
    time.sleep(0.5)
    onboard_led.on()

