from wifi import connect_wifi
from signal import blink
from mqtt import mqtt_main

WIFI_SSID = "mynet_ASUS"
WIFI_KEY = ""

MQTT_CLIENT_ID = "esp_1"
MQTT_CLIENT_USER = "esp_1"
MQTT_CLIENT_PWD = "PyConSK2022"

MQTT_CLIENT_SERVER = "node02.myqtthub.com"
MQTT_CLIENT_SUB_TOPICS = ["esp_1/led"]

MQTT_LOOP = False

connect_wifi(WIFI_SSID, WIFI_KEY)

def msg_callback(topic, msg):
    # blink on D2 -> GPIO4
    if topic == b"esp_1/led":
        blink(1, gpio=4)

if MQTT_LOOP:
    mqtt_main(
        MQTT_CLIENT_ID,
        MQTT_CLIENT_SERVER,
        MQTT_CLIENT_USER,
        MQTT_CLIENT_PWD,
        MQTT_CLIENT_SUB_TOPICS,
        msg_callback
    )