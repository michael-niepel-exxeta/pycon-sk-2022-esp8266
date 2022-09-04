from mqtt_as import MQTTClient, config
import uasyncio as asyncio
from machine import Pin
from blink import blink_onboard

def callback(topic, msg, retained):
    print((topic, msg, retained))
    blink_onboard(1)

async def conn_han(client):
    await client.subscribe('esp_1/led', 1)

async def main(client):
    connected = False
    while not connected:
        try:
            connected = not await client.connect()
        except OSError as e:
            pass

    ir_sensor = Pin(4, Pin.IN)
    was_on = False
    while True:
        ir_sensor_on = not ir_sensor.value() # 0 is "ON"
        await asyncio.sleep(0.1)
        if ir_sensor_on and not was_on:
            was_on = True
            print('ir_sensor_on', ir_sensor_on)
            await client.publish('esp_1/ir_sensor', f'{ir_sensor_on}', qos = 1)
        if not ir_sensor_on:
            was_on = False


config['subs_cb'] = callback
config['connect_coro'] = conn_han

MQTTClient.DEBUG = True
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()