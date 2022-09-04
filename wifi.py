import network
import gc
from signal import blink_onboard


def connect_wifi(ssid, key):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, key)
        while not wlan.isconnected():
            pass

    blink_onboard(1)
    print('network config:', wlan.ifconfig())
    gc.collect()