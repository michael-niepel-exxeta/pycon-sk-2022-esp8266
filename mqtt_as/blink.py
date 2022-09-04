import time
from machine import Pin

def blink_onboard(times=1):
    led = Pin(2, Pin.OUT)
    for _ in range(times):
        led.off() # is on
        time.sleep(0.5)
        led.on() # is off
        time.sleep(0.5)