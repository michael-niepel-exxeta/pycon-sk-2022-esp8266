import time
from signal import blink_onboard


def connect_and_subscribe(client_id, server, user, pwd, topics_sub, sub_cb):
    from umqtt.simple import MQTTClient
    client = MQTTClient(client_id, server, ssl=False, user=user, password=pwd)
    client.set_callback(sub_cb)
    connected = False
    while not connected:
        try:
            connected = not client.connect() # zero when OK
            time.sleep(0.5)
        except OSError as e:
            pass
    for topic in topics_sub:
        client.subscribe(topic)
    gc.collect()
    return client


def mqtt_main(client_id, server, user, pwd, topics_sub, sub_cb):
    client = connect_and_subscribe(client_id, server, user, pwd, topics_sub, sub_cb)
    while True:
        client.check_msg()
        time.sleep(1)
        blink_onboard(1)