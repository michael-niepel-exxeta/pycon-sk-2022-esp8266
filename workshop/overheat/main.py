import json
from mqtt_as import MQTTClient, config
from config import wifi_led, blue_led  # Local definitions
import uasyncio as asyncio
import onewire
import ds18x20
from machine import Pin

SERVER = 'node02.myqtthub.com'

TEMP_STEP = 1
TRACK_ID = 0

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
    ow = onewire.OneWire(Pin(4))
    ds = ds18x20.DS18X20(ow)
    roms = ds.scan()
    
    temp = 0
    while True:
        await asyncio.sleep_ms(250)
        ds.convert_temp()
        for rom in roms:
            new_temp = ds.read_temp(rom)
        print(new_temp)
        if abs(temp-new_temp) > TEMP_STEP:
            temp = new_temp
            msg = {
                "track": TRACK_ID,
                "temp": f"{temp}"
            }
            await client.publish('racetrack/overheat', json.dumps(msg), qos = 1)

# Define configuration
config['wifi_coro'] = wifi_han
config['connect_coro'] = conn_han
config['server'] = SERVER

# Credentials
config['user'] = 'esp_3'
config['password'] = 'PyConSK2022'
config['client_id'] = 'esp_3'

# Set up client
MQTTClient.DEBUG = True  # Optional
client = MQTTClient(config)

asyncio.create_task(heartbeat())
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
    asyncio.new_event_loop()