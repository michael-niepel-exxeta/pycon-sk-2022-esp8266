import json
from mqtt_as import MQTTClient, config
from config import wifi_led, blue_led  # Local definitions
import uasyncio as asyncio
from hcsr04 import HCSR04

SERVER = 'node02.myqtthub.com'

DISTANCE_SENSOR = HCSR04(12, 14)
DISTANCE_STEPS_CM = 2
MAX_DISTANCE = 50


TRACK_ID = 0

async def heartbeat():
    s = True
    while True:
        await asyncio.sleep_ms(500)
        blue_led(s)
        s = not s

async def wifi_han(state):
    wifi_led(not state)
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
    distance = 0
    while True:
        await asyncio.sleep_ms(100)
        new_distance = DISTANCE_SENSOR.distance_cm()
        # clamp to max distance
        new_distance = max(0, min(new_distance, MAX_DISTANCE))
        print(f"Measured distance: {new_distance}")
        if abs(distance - new_distance) > DISTANCE_STEPS_CM:
            distance = new_distance
            msg = {
                "track": TRACK_ID,
                "distance": int(distance)
            }
            print(f"Publishing: {msg}")
            await client.publish('racetrack/distance', json.dumps(msg), qos = 1)

# Define configuration
config['wifi_coro'] = wifi_han
config['connect_coro'] = conn_han
config['server'] = SERVER

# Credentials
config['user'] = 'esp_1'
config['password'] = 'PyConSK2022'
config['client_id'] = 'esp_1'

# Set up client
MQTTClient.DEBUG = True  # Optional
client = MQTTClient(config)

asyncio.create_task(heartbeat())
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
    asyncio.new_event_loop()