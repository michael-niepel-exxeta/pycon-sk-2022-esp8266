import json
from mqtt_as import MQTTClient, config
from config import wifi_led, blue_led  # Local definitions
import uasyncio as asyncio
from machine import Pin
from machine import RTC
import ntptime

SERVER = 'node02.myqtthub.com'

TRACK_ID = 0

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

async def conn_han(_):
    wifi_led(True)
    print('Client connected')

async def main(client):
    try:
        await client.connect()
    except OSError:
        print('Connection failed.')
        return
    ir_sensor = Pin(4, Pin.IN)
    ir_sensor2 = Pin(5, Pin.IN)
    rtc = RTC()
    # sync time
    ntptime.settime()
    was_on_1 = False
    was_on_2 = False
    while True:
        await asyncio.sleep_ms(5)
        ir_sensor_on = not ir_sensor.value() # 0 is "ON"
        if ir_sensor_on and not was_on_1:
            now = rtc.datetime()
            was_on_1 = True
            msg = {
                "track": 0,
                "lap": time_from_timetuple(now)
            }
            await client.publish('racetrack/lap', json.dumps(msg), qos = 1)
        if not ir_sensor_on:
            was_on_1 = False
        # second sensor
        ir_sensor2_on = not ir_sensor2.value() # 0 is "ON"
        if ir_sensor2_on and not was_on_2:
            now = rtc.datetime()
            was_on_2 = True
            msg = {
                "track": 1,
                "lap": time_from_timetuple(now)
            }
            await client.publish('racetrack/lap', json.dumps(msg), qos = 1)
        if not ir_sensor2_on:
            was_on_2 = False

# Define configuration
config['wifi_coro'] = wifi_han
config['connect_coro'] = conn_han
config['server'] = SERVER

# Credentials
config['user'] = 'esp_2'
config['password'] = 'PyConSK2022'
config['client_id'] = 'esp_2'

# Set up client
MQTTClient.DEBUG = True  # Optional
client = MQTTClient(config)

asyncio.create_task(heartbeat())
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
    asyncio.new_event_loop()