import paho.mqtt.client as paho
from paho import mqtt

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"CONNACK received with code {rc}.")

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print(f"mid: {str(mid)}")

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print(f"Subscribed: {str(mid)} {str(granted_qos)}")

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(f"{msg.topic} {str(msg.qos)} {str(msg.payload)}")

# MQTTv31 for myqtthub
client = paho.Client(client_id="api_server", userdata=None, protocol=paho.MQTTv31)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("api_server", "PyConSK2022")

client.connect("node02.myqtthub.com", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics
client.subscribe("esp_1/#", qos=1)

# a single publish
client.publish("esp_1/led", payload="ON", qos=1)

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
client.loop_forever()