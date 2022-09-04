import time
from umqtt.simple import MQTTClient

def msg_callback(topic, msg):
    print(topic, msg)

client = MQTTClient("esp_1","node02.myqtthub.com", ssl=False, user="esp_1", password="PyConSK2022")
client.set_callback(msg_callback)
client.connect() # might fail
client.subscribe("esp_1/led")

client.publish("esp_1/temp", "25")

while True:
    client.check_msg() # client.wait_msg() blocking
    time.sleep(1)



