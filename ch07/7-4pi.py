import io
import cv2
import paho.mqtt.client as mqtt

broker_ip = "localhost"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(broker_ip, 1883)
client.loop_start()

camera = cv2.VideoCapture(0, cv2.CAP_V4L)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

buffer_size = 1
camera.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)

while True:
	key = input("사진촬영계속? (종료는 stop 입력)>>")
	if(key == "stop"):
		break
	for i in range(buffer_size+1):
		ret, frame = camera.read()

	im_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
	client.publish("jpeg", im_bytes, qos=0)

camera.release()
client.loop_stop()
client.disconnect()
