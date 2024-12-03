import paho.mqtt.client as mqtt

broker_ip = "localhost"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(broker_ip, 1883)
client.loop_start()

while True:
	temperature = input("온도>>>")
	temperature = int(temperature)
	if temperature == 0:
		break
	client.publish("room/temp", temperature)

client.loop_stop()
client.disconnect()
print("프로그램 종료")
