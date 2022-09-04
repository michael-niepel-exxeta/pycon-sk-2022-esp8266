from mqtt_as import MQTTClient
from config import config, blue_led, wifi_led, green_led, yellow_led, red_led
import uasyncio as asyncio
import json

SERVER = 'node02.myqtthub.com'

RUNNING_CMD = None

def reset():
    green_led(False)
    yellow_led(False)
    red_led(False)

async def ready_set_go():
    red_led(1)
    await asyncio.sleep_ms(1000)
    red_led(0)
    yellow_led(1)
    await asyncio.sleep_ms(1000)
    yellow_led(0)
    green_led(1)
    await asyncio.sleep_ms(1000)
    green_led(0)

async def blink_red():
    s = True
    while True:
        await asyncio.sleep_ms(500)
        red_led(s)
        s = not s

async def heartbeat():
    s = True
    while True:
        await asyncio.sleep_ms(500)
        blue_led(s)
        s = not s

def sub_cb(topic, msg, retained):
    print((topic, msg, retained))
    global RUNNING_CMD
    # just cancel anything running
    if RUNNING_CMD is not None:
        RUNNING_CMD.cancel()
    msg = json.loads(msg)
    command = msg.get('command', 'rsg')
    if command == 'rsg':
        RUNNING_CMD = asyncio.create_task(ready_set_go())
    elif command == 'blink_red':
        RUNNING_CMD = asyncio.create_task(blink_red())
    elif command == 'reset':
        reset()

async def wifi_han(state):
    wifi_led(not state)
    print('Wifi is ', 'up' if state else 'down')
    await asyncio.sleep(1)

async def conn_han(client):
    await client.subscribe('racetrack/lights', 1)

async def main(client):
    await client.connect()
    n = 0
    await asyncio.sleep(2)
    # Keep loop running
    while True:
        print('heartbeat', n)
        # We publish some stuff here
        n += 1
        await asyncio.sleep(20)

# Define configuration
config['subs_cb'] = sub_cb
config['server'] = SERVER
config['connect_coro'] = conn_han
config['wifi_coro'] = wifi_han

# Credentials
config['user'] = 'esp_4'
config['password'] = 'PyConSK2022'
config['client_id'] = 'esp_4'

# Set up client
MQTTClient.DEBUG = True  # Optional
client = MQTTClient(config)

reset()
asyncio.create_task(heartbeat())
try:
    asyncio.run(main(client))
finally:
    client.close()
    asyncio.new_event_loop()