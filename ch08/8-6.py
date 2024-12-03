import time
import RPi.GPIO as GPIO

try:
	def measure_distance(tring, echo):
		time.sleep(0.2)
		GPIO.output(trig, 1)
		GPIO.output(trig, 0)
		
		while(GPIO.input(echo) == 0):
			pass

		pulse_start = time.time()
		while(GPIO.input(echo) == 1):
			pass

		pulse_end = time.time()
		pulse_duration = pulse_end - pulse_start
		return pulse_duration*340*100/2

	trig = 20
	echo = 16
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(trig, GPIO.OUT)
	GPIO.setup(echo, GPIO.IN)

	while True:
		distance = measure_distance(trig, echo)
		time.sleep(0.5)
		print("물체와의 거리는 %fcm 입니다." % distance)

except KeyboardInterrupt:
	print("Control C shoutup")
finally:
	print("cleanup")
	GPIO.cleanup()
