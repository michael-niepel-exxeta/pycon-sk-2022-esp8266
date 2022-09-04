from sys import platform
from machine import Pin
from mqtt_as import config

# Not needed if you're only using ESP8266
config['ssid'] = 'mynet_EXT'
config['wifi_pw'] = ''


def ledfunc(pin):
    pin = pin
    def func(v):
        pin(not v)
    return func
blue_led = ledfunc(Pin(2, Pin.OUT, value = 1))

if platform == 'esp8266':
    # onboard blue led
    wifi_led = ledfunc(Pin(16, Pin.OUT, value = 1))
elif platform == 'esp32':
    # pin 4 - D4
    wifi_led = ledfunc(Pin(4, Pin.OUT, value = 1))
else:
    wifi_led = blue_led