import json
from mqtt_as import MQTTClient, config
from config import wifi_led, blue_led  # Local definitions
import uasyncio as asyncio
from machine import Pin
from machine import RTC
import ntptime

SERVER = 'node02.myqtthub.com'

BUTTON = Pin(14, Pin.IN, Pin.PULL_UP) # 0 is ON
LED = Pin(4, Pin.OUT, 0)

def time_from_timetuple(timetuple) -> str:
    return f"{timetuple[4]}:{timetuple[5]}:{timetuple[6]}.{timetuple[7]}"

async def heartbeat():
    s = True
    while True:
        await asyncio.sleep_ms(500)
        blue_led(s)
        s = not s

async def wifi_han(state):
    # wifi_led(not state)
    print('Wifi is ', 'up' if state else 'down')
    await asyncio.sleep(1)

def sub_cb(topic, msg, retained):
    print((topic, msg, retained))
    ntptime.settime()

async def conn_han(_):
    print('Client connected')
    wifi_led(True)
    await client.subscribe('racetrack/sync_time', 1)

async def main(client):
    try:
        await client.connect()
    except OSError:
        print('Connection failed.')
        return
    rtc = RTC()
    # sync time
    ntptime.settime()
    was_on = False
    while True:
        await asyncio.sleep_ms(10)
        button_on = not BUTTON.value()
        LED.value(button_on)
        # pub when we release the button
        if not button_on and was_on:
            now = rtc.datetime()
            was_on = False
            msg = {
                "time": time_from_timetuple(now)
            }
            await client.publish('racetrack/button', json.dumps(msg), qos = 1)
        if button_on:
            was_on = True
        

# Define configuration
config['wifi_coro'] = wifi_han
config['subs_cb'] = sub_cb
config['connect_coro'] = conn_han
config['server'] = SERVER

# Credentials
config['user'] = 'esp_6'
config['password'] = 'PyConSK2022'
config['client_id'] = 'esp_6'

# Set up client
MQTTClient.DEBUG = True  # Optional
client = MQTTClient(config)

asyncio.create_task(heartbeat())
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
    asyncio.new_event_loop()