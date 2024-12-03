import paho.mqtt.client as mqtt

ip = input("브로커의 IP 주소>>")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(ip, 1883)
client.loop_start()

while True:
	message = input("문자메시지>>")
	if message == "exit":
		break
	client.publish("letter", message)
	print("메시지 전송: %s" % message)

client.loop_stop()
client.disconnect()
