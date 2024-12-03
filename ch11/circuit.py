import time
import RPi.GPIO as GPIO

# LED를 켜고 끄는 함수
def controlLED(on_off): #led 번호의 핀에 on_off(0/1) 값 출력하는 함수
  global led
  GPIO.output(led, on_off)

#초음파 센서를 제어하여 물체와의 거리를 측정하여 거리 값을 리턴하는 함수
def measure_distance():
  global trig, echo
  time.sleep(0.2) # 초음파 센서의 준비 시간을 위해 200밀리초 지연
  GPIO.output(trig, 1) # trig 핀에 1 출력
  GPIO.output(trig, 0) # trig 핀에 0 출력 High->low. 초음파 발사 지시

  while (GPIO.input(echo) == 0): # echo 핀 값이 0->1로 바뀔 때까지 루프
    pass

  # echo 핀 값이 1이면 초음파가 발사되었음
  pulse_start = time.time() # 초음파 발사 시간 기록
  while(GPIO.input(echo) == 1): # echo 핀 값이 1->0으로 바뀔 때까지 루프
    pass

  # echo 핀 값이 0이 되면 초음파 수신하였음
  pulse_end = time.time() # 초음파가 되돌아 온 시간 기록
  pulse_duration = pulse_end - pulse_start # 경과 시간 계산
  return pulse_duration*340*100/2

# 초음파 센서를 다루기 위한 전역 변수 선언 및 초기화
trig = 20
echo = 16
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

#LED를 다루기 위한 전역 변수 선언 및 초기화
led = 6
GPIO.setup(led, GPIO.OUT)