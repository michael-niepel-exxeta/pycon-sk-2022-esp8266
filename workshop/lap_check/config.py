from sys import platform
from machine import Pin
from mqtt_as import config

# Not needed if you're only using ESP8266
config['ssid'] = 'PyconSK'
config['wifi_pw'] = 'FIITpyconsk2022'


def ledfunc(pin):
    pin = pin
    def func(v):
        if platform == 'esp8266':
            pin(not v)
        else:
            pin(v)
    return func
blue_led = ledfunc(Pin(2, Pin.OUT, value = 0))

if platform == 'esp8266':
    # onboard blue led
    wifi_led = ledfunc(Pin(16, Pin.OUT, value = 0))
elif platform == 'esp32':
    # pin 4 - D4
    wifi_led = ledfunc(Pin(4, Pin.OUT, value = 0))
else:
    wifi_led = blue_led