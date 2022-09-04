MyQttHub
--------

https://node02.myqtthub.com/devices

```code python
# IP works better
c = MQTTClient("esp_1", "185.195.98.58", ssl=False, user="esp_1", password="PyConSK2022")
# can connect to domain as well but takes some time
c = MQTTClient("esp_1", "node02.myqtthub.com", ssl=False, user="esp_1", password="PyConSK2022")
```


HiveMQ Cloud
------------

```code python
# SSL missing cert ;)
# c = MQTTClient("ashjdb", "f3821d0075364879b1e2bd44c4bb2975.s1.eu.hivemq.cloud", ssl=True, user="pycon_esp_1", password="PyConSK2022")
```


Localhost
---------
```code python
c = MQTTClient("pycon_esp_1", "192.168.100.158", keepalive=30)
```
