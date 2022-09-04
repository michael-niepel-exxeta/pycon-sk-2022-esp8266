from mqtt_as import MQTTClient
from config import config, blue_led, wifi_led
import uasyncio as asyncio
import json
from ds1803 import DS1803


SERVER = 'node02.myqtthub.com'
GLOBAL_DS1803 = DS1803() # Default pins

async def reset_pots():
    global GLOBAL_DS1803
    GLOBAL_DS1803.set_pot0_value(0)
    GLOBAL_DS1803.set_pot1_value(0)


async def set_pot_value_async(pot: int, value: int):
    global GLOBAL_DS1803
    if pot == 0:
        GLOBAL_DS1803.set_pot0_value(value)
    elif pot == 1:
        GLOBAL_DS1803.set_pot1_value(value)
    await asyncio.sleep_ms(10)

async def heartbeat():
    s = True
    while True:
        await asyncio.sleep_ms(500)
        blue_led(s)
        s = not s

def sub_cb(topic, msg, retained):
    print((topic, msg, retained))
    msg = json.loads(msg)
    track = int(msg.get("track"))
    speed = int(msg.get("speed"))
    asyncio.create_task(set_pot_value_async(track, speed))
    # if track == "0":
    #     GLOBAL_DS1803.set_pot0_value(speed)
    # elif track == "1":
    #     GLOBAL_DS1803.set_pot1_value(speed)

async def wifi_han(state):
    # wifi_led(not state)
    print('Wifi is ', 'up' if state else 'down')
    await asyncio.sleep(1)

async def conn_han(client):
    wifi_led(True)
    await client.subscribe('racetrack/speed', 1)

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
config['user'] = 'esp32_1'
config['password'] = 'PyConSK2022'
config['client_id'] = 'esp32_1'

# Set up client
MQTTClient.DEBUG = True  # Optional
client = MQTTClient(config)

asyncio.create_task(heartbeat())
try:
    asyncio.run(main(client))
finally:
    client.close()
    asyncio.new_event_loop()