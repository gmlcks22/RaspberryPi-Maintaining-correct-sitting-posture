import time
import RPi.GPIO as GPIO
from adafruit_htu21d import HTU21D
import busio

try:
	def led_on_off(pin, value):
		GPIO.output(pin, value)

	def getTemperature(sensor):
		return float(sensor.temperature)

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	led = 6
	GPIO.setup(led, GPIO.OUT)

	sda = 2
	scl = 3

	i2c = busio.I2C(scl, sda)
	sensor = HTU21D(i2c)

	THRESHOLD = 26
	prev_temp = 0
	while True:
		cur_temp = getTemperature(sensor)
		if prev_temp < THRESHOLD and cur_temp >= THRESHOLD:
			led_on_off(led, 1)
		elif prev_temp >= THRESHOLD and cur_temp < THRESHOLD:
			led_on_off(led, 0)
		else:
			pass
		print("현재 온도는 %4.1d" % cur_temp)
		prev_temp = cur_temp
		time.sleep(1)
except KeyboardInterrupt:
	print("Ctrl C end")
finally:
	print("cleanup")
	GPIO.cleanup()
