import time
import RPi.GPIO as GPIO
import Adafruit_MCP3008

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

mcp = Adafruit_MCP3008.MCP3008(clk=11, cs=8, miso=9, mosi=10)

while True:
	print(mcp.read_adc(0))
	time.sleep(1)
