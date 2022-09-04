import time

def blink(times=1, gpio=4):
    import machine
    onboard_led = machine.Pin(gpio, machine.Pin.OUT)
    for _ in range(times):
        onboard_led.on()
        time.sleep(0.5)
        onboard_led.off()
        time.sleep(0.5)


def blink_onboard(times=1):
    import machine
    onboard_led = machine.Pin(2, machine.Pin.OUT)
    for _ in range(times):
        # onboard led is the other way around
        onboard_led.off()
        time.sleep(0.5)
        onboard_led.on()
        time.sleep(0.5)