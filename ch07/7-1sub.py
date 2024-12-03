import paho.mqtt.client as mqtt

def on_connect(client, userdata, flag, rc, prop=None):
	print("접속 결과: " + str(rc))
	client.subscribe("letter")

def on_message(client, userdata, msg):
	print(msg.topic, end=", ")
	print(str(msg.payload.decode("utf-8")))

ip = input("브로커의 IP 주소>>")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(ip, 1883)
client.loop_forever()

