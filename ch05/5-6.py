import cv2

camera = cv2.VideoCapture(0, cv2.CAP_V4L)

# 프레임 크기를 640*480으로 하고, camera가 카메라로부터 읽어오는 주기(FPS)를 10으로 설정
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_FPS, 10)

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
writer = cv2.VideoWriter("video_5_6.avi", fourcc, 10, (640, 480))

while True:
	ret, image = camera.read()
	if ret == True:
		cv2.imshow('preview', image)
		writer.write(image)
	else:
		print('카메라로부터 프레임의 캡쳐할 수 없습니다.')
		break
	
	# 1 밀리초 동안 ESC 키 입력을 기다린다.
	if cv2.waitKey(1) ==27:
		break

writer.release()
camera.release()
cv2.destroyAllWindows()

