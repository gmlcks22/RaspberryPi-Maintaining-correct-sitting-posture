import RPi.GPIO as GPIO
import time

try:
	def button_pressed(channel):
		print("%d 핀에 연결된 스위치 눌러짐" % channel)

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	button = 21
	GPIO.setup(button, GPIO.IN, GPIO.PUD_DOWN)

	GPIO.add_event_detect(button, GPIO.RISING, button_pressed, bouncetime=10)
	while True:
		pass
except KeyboardInterrupt:
	print("Ctrl + c 종료")
finally:
	print("cleanup")
	GPIO.cleanup()
