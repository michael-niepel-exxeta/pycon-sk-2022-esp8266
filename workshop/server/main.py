import asyncio
from contextlib import AsyncExitStack
import json
from asyncio_mqtt import Client, MqttError
from contextlib import suppress
from racetrack import Racetrack, TrackState
import requests

# pub
SPEED_TOPIC = "speed"
LIGHTS_TOPIC = "lights"
SYNC_TIME_TOPIC = "sync_time"

# sub
DISTANCE_TOPIC = "distance"
LAP_TOPIC = "lap"
OVERHEAT_TOPIC = "overheat"
BUTTON_TOPIC = "button"

TOPIC_ROOT = "racetrack"
LOG_FORMAT = "Received: {}"

# racetrack state
RACETRACK = None

LEADERBOARD_API_URL = "http://localhost:8000/leaderboard/"

async def racetrack():
    # Context manager
    async with AsyncExitStack() as stack:
        tasks = set()
        stack.push_async_callback(cancel_tasks, tasks)

        # Connect to the MQTT broker
        client = Client("node02.myqtthub.com",
                        client_id="api_server",
                        username="api_server",
                        password="PyConSK2022")
        await stack.enter_async_context(client)

        sub_to = [DISTANCE_TOPIC, LAP_TOPIC, OVERHEAT_TOPIC, BUTTON_TOPIC]
        topic_filters = [(f"{TOPIC_ROOT}/{topic}", topic) for topic in sub_to]
        for topic_filter, topic in topic_filters:
            manager = client.filtered_messages(topic_filter)
            messages = await stack.enter_async_context(manager)
            task = asyncio.create_task(
                on_message_received(client, messages, topic))
            tasks.add(task)

        # Subscribe to everything in racetrack/...
        await client.subscribe(f"{TOPIC_ROOT}/#")

        await init_track(client)

        # Wait for everything to complete (or fail due to, e.g., network
        # errors)
        await asyncio.gather(*tasks)


async def init_track(client):
    global RACETRACK
    RACETRACK = Racetrack()
    # stop tracks
    msg = {"track": 0, "speed": 0}
    await publish_speed(client, msg)
    msg = {"track": 1, "speed": 0}
    await publish_sync_time(client)
    await publish_speed(client, msg)
    await publish_lights(client, {"command": "blink_red"})

async def start_race(client, time):
    await publish_lights(client, {"command": "rsg"})
    await publish_sync_time(client)
    await asyncio.sleep(3)
    RACETRACK.start_race(time)
    msg = {"track": 0, "speed": Racetrack.INITIAL_SPEED}
    await publish_speed(client, msg)
    msg = {"track": 1, "speed": Racetrack.INITIAL_SPEED}
    await publish_speed(client, msg)

async def stop_race(client):
    RACETRACK.stop_race()
    await publish_lights(client, {"command": "blink_red"})
    msg = {"track": 0, "speed": 0}
    await publish_speed(client, msg)
    msg = {"track": 1, "speed": 0}
    await publish_speed(client, msg)
    await publish_sync_time(client)

async def publish_speed(client, message: dict):
    print(f"Publish: {message}")
    await client.publish(f"{TOPIC_ROOT}/{SPEED_TOPIC}",
                         json.dumps(message),
                         qos=1)


async def publish_lights(client, message: dict):
    print(f"Publish: {message}")
    await client.publish(f"{TOPIC_ROOT}/{LIGHTS_TOPIC}",
                         json.dumps(message),
                         qos=1)

async def publish_sync_time(client):
    await client.publish(f"{TOPIC_ROOT}/{SYNC_TIME_TOPIC}",
                         b"True",
                         qos=1)

async def post_results(elapsed_seconds):
    print(f"Posting to leaderboard: {elapsed_seconds}")
    try:
        requests.post(LEADERBOARD_API_URL, data=json.dumps({
            "time": elapsed_seconds
        }))
    except Exception as e:
        print(f"Unable to post time: {str(e)}")

async def on_message_received(client, messages, topic):
    global RACETRACK
    # based on topics
    async for message in messages:
        print(LOG_FORMAT.format(message.payload.decode()))
        decoded_message = json.loads(message.payload.decode())
        # control speed
        if topic == DISTANCE_TOPIC:
            if RACETRACK.STATE == TrackState.RUNNING:
                track_id = decoded_message.get("track")
                speed_message = {
                    "track": track_id,
                    "speed": RACETRACK.speed_from_distance(decoded_message.get("distance"), track_id)
                }
                await publish_speed(client, speed_message)
        elif topic == BUTTON_TOPIC:
            time = decoded_message.get("time")
            if RACETRACK.STATE == TrackState.IDLE:
                await start_race(client, time)
            # publish initial speeds
            elif RACETRACK.STATE == TrackState.RUNNING:
                await stop_race(client)
        elif topic == LAP_TOPIC:
            if RACETRACK.STATE == TrackState.RUNNING:
                track_id, elapsed_seconds = RACETRACK.lap(decoded_message.get("track"), time=decoded_message.get("lap"))
                if  track_id != -1:
                    print(f">>>> {track_id} wins!")
                    await stop_race(client)
                    await post_results(elapsed_seconds)
        elif topic == OVERHEAT_TOPIC:
            temp = float(decoded_message.get("temp"))
            track_id = decoded_message.get("track")
            if RACETRACK.STATE == TrackState.RUNNING:
                if temp >= Racetrack.OVERHEAT_IN_C:
                    RACETRACK.overheat(track_id)
                else:
                    RACETRACK.overheat(track_id, False)


async def cancel_tasks(tasks):
    for task in tasks:
        if task.done():
            continue
        with suppress(asyncio.CancelledError):
            task.cancel()
            await task


async def main():
    # Run the racetrack indefinitely. Reconnect automatically
    # if the connection is lost.
    reconnect_interval = 3  # [seconds]
    while True:
        try:
            await racetrack()
        except MqttError as error:
            print(
                f'Error "{error}". Reconnecting in {reconnect_interval} seconds.'
            )
        finally:
            await asyncio.sleep(reconnect_interval)


asyncio.run(main())