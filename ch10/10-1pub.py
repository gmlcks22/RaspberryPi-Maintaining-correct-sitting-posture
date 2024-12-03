import time
import paho.mqtt.client as mqtt

ip = "localhost"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(ip, 1883)
client.loop_start()

count = 0
while True:
  message = input("문자메시지>>") # 사용자로부터 문자열 입력
  if message == "exit":
    break
  client.publish("letter", message) # letter 토픽화 함꼐 메시지 전송
  print("메시지 전송: %s" % message)

client.loop_stop()
client.disconnect()
