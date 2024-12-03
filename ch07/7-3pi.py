import paho.mqtt.client as mqtt
import time
import random

flag = "stop"

def on_connect(client, userdata, flag, rc, prop=None):
	client.subscribe("command")

def on_message(client, userdata, msg):
	global flag
	command = msg.payload.decode('utf-8')
	if command == "start":
		flag = "start"
		print("온도 전송...")
	elif command == "stop":
		flag = "stop"
		print("\n전송 중단...")
	else:
		print("명령 오류: ", command)

broker_ip = "localhost"
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_ip, 1883)
client.loop_start()

print("시작 명령 대기...")
while True:
	if flag == "start":
		temperature = random.randint(0, 40)
		client.publish("room/temp", temperature)
		print(temperature, end=" ", flush=True)
	time.sleep(2)

client.loop_stop()
client.disconnect()
print("프로그램 종료")

