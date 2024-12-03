import time
import RPi.GPIO as GPIO
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

try:
    # pin에 연결된 led에 value(0/1) 값을 출력하여 LED를 키거나 끄는 함수
    def led_on_off(pin, value):
        GPIO.output(pin, value)

    GPIO.setmode(GPIO.BCM)  # BCM모드로 핀 번호 매기기
    GPIO.setwarnings(False)  # 경고글이 출력되지 않게 설정

    first_led = 6
    GPIO.setup(first_led, GPIO.OUT)  # 하얀색 led GPIO 6 핀을 출력으로 지정
    second_led = 5
    GPIO.setup(second_led, GPIO.OUT)  # 노란색 led GPIO 5 핀을 출력으로 지정

    on = 1
    off = 0

    # 거리를 측정해
    def measure_distance(trig, echo):
        time.sleep(0.2)
        GPIO.output(trig, 1)
        time.sleep(0.00001) #초음파 지연 추가
        GPIO.output(trig, 0)

        # echo 핀 값이 0->1로 바뀔 때까지 루프
        while GPIO.input(echo) == 0:
            pass

        # echo 핀 값이 1이면 초음파가 발사되었음
        pulse_start = time.time()
        while GPIO.input(echo) == 1:
            pass

        # echo 핀 값이 0이 되면 초음파 수신하였음
        pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        return pulse_duration * 340 * 100 / 2

    trig = 20  # GPIO 20
    echo = 16  # GPIO 16
    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)

    while True:
        distance = measure_distance(trig, echo)
        time.sleep(0.5)  # 0.5초 간격으로 거리 측정
        print("물체와의 거리는 %fcm 입니다." % distance)
        if distance <= 20 and distance > 10:
            led_on_off(first_led, on)
        elif distance <= 10:
            led_on_off(first_led, on)
            led_on_off(second_led, on)
            for i in range(buffer_size+1):
                ret, frame = camera.read()

                im_bytes = cv2.imencode('.jpg', frame)[1].tobytes() # byte배열로 저장
                client.publish("jpeg", im_bytes, qos = 0)

        else:
            led_on_off(first_led, off)
            led_on_off(second_led, off)

except KeyboardInterrupt:
    print("Control C shutup")
finally:
    camera.release() # 카메라 사용 끝내기
    client.loop_stop() # 메시지 루프를 실행하는 스레드 종료
    client.disconnect()
    print("cleanup")
    GPIO.cleanup()
