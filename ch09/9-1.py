import time
import RPi.GPIO as GPIO
from adafruit_htu21d import HTU21D
import busio

try:
	def getTemperature(sensor):
		return float(sensor.temperature)
	def getHumidity(sensor):
		return float(sensor.relative_humidity)

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	sda = 2
	scl = 3

	i2c = busio.I2C(scl, sda)
	sensor = HTU21D(i2c)

	while True:
		print("현재 온도는  %4.1d" % getTemperature(sensor))
		print("현재 습도는 %4.1d %%" % getHumidity(sensor))
		time.sleep(1)
except KeyboardInterrupt:
	print("ctrl C end")
finally:
	print("cleanup")
	GPIO.cleanup()

