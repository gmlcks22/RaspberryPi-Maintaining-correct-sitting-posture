import time
import RPi.GPIO as GPIO

try:
	def led_on_off(pin, value):
		GPIO.output(pin, value)

	def button_pressed(pin):
		global btn_status
		global led
		btn_status = 0 if btn_status == 1 else 1
		led_on_off(led, btn_status)

	led = 6
	button = 21
	btn_status = 0 # 현재 버튼이 눌려진 상태, 1이면 눌러져 있음

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(led, GPIO.OUT)
	GPIO.setup(button, GPIO.IN, GPIO.PUD_DOWN)

	GPIO.add_event_detect(button, GPIO.RISING, button_pressed, 10)

	print("스위치를 누르면 LED가 On되고 다시 누르면 Off 됩니다.")

	while True:
		pass

except KeyboardInterrupt:
	print("Ctrl + c 종료")
finally:
	print("cleanup")
	GPIO.cleanup()		
	
