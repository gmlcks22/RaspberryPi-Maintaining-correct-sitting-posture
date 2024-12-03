import time
import RPi.GPIO as GPIO

try:
	def led_on_off(pin, value):
		GPIO.output(pin, value)

	GPIO.setmode(GPIO.BCM)

	GPIO.setwarnings(False)

	led = 6
	GPIO.setup(led, GPIO.OUT)

	button = 21
	GPIO.setup(button, GPIO.IN, GPIO.PUD_DOWN)

	print("스위치를 누르고 있는 동안 LED가 켜지고 놓으면 꺼집니다.")

	while True:
		status = GPIO.input(button)
		led_on_off(led, status)

except KeyboardInterrupt:
	print("Ctrl + c 종료")
finally:
	print("cleanup()")
	GPIO.cleanup()
