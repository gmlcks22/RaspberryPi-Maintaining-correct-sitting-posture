import time
import RPi.GPIO as GPIO

try:
	def increase(pwm):
		print("increase the light")
		for value in range(0, 100):
			pwm.ChangeDutyCycle(value)
			time.sleep(0.05)

	def decrease(pwm):
		print("decrease the light")
		for value in range(99, -1, -1):
			pwm.ChangeDutyCycle(value)
			time.sleep(0.05)
	
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	led = 6
	GPIO.setup(led, GPIO.OUT)

	GPIO.output(led, GPIO.LOW)
	pwm = GPIO.PWM(led, 100)
	pwm.start(0)
	while True:
		increase(pwm)
		decrease(pwm)

except KeyboardInterrupt:
	print("Ctrl C shutup")
finally:
	print("cleanup")
	GPIO.cleanup()
			
