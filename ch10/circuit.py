import time
import RPi.GPIO as GPIO

def controlLED(on_off):
  global led
  GPIO.output(led, on_off)

def measure_distance():
  global trig, echo
  time.sleep(0.2) # 초음파 센서의 준비 시간을 위해 200 밀리초 지연
  GPIO.output(trig, 1) # trig 핀에 1(High) 출력.
  time.sleep(0.00001)
  GPIO.output(trig, 0) # trig 핀에 0(low) 출력.

  while(GPIO.input(echo) == 0): #echo 핀 값이 0->1로 바뀔 때까지 루프
    pass

  # echo 핀 값이 1이면 초음파가 발사되었음
  pulse_start = time.time()
  while(GPIO.input(echo) == 1):
    pass

  # echo 핀 값이 0이 되면 초음파 수신하였음
  pulse_end = time.time()
  pulse_duration = pulse_end - pulse_start # 경과 시간 계산
  return pulse_duration*340*100/2 # 거리 계산하여 리턴(단위 cm)
  
# 초음파 센서를 다루기 위한 전역 변수 선언 및 초기화
trig = 20 #GPIO 20
echo = 16 #GPIO 16
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)


#LED를 다루기 위한 전역 변수 선언 및 초기화
led = 6 #GPIO 6
GPIO.setup(led, GPIO.OUT) # GPIO 6 핀을 출력으로 지정
