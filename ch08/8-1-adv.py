import time
import RPi.GPIO as GPIO

try:
	def led_on_off(pin, value):
		GPIO.output(pin, value)

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	led=6
	GPIO.setup(led, GPIO.OUT)

	on_off = 1
	print("LED를 지켜보세요.")

	for i in range(5):
		led_on_off(led, on_off)
		time.sleep(1)
		print(i, end=" ", flush=True)
		on_off = 0 if on_off == 1 else 1

except KeyboardInterrupt:
	print("Ctrl + c 종료")
finally:
	print("cleanup()")
	GPIO.cleanup()

