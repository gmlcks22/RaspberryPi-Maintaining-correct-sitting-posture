import cv2

camera = cv2.VideoCapture(0, cv2.CAP_V4L) #카메라 객체 생성
camera.set(cv2.CAP_PROP_BUFFERSIZE, 10) #set buffer size to 10

def take_picture():
	size = camera.get(cv2.CAP_PROP_BUFFERSIZE)
	while size>0:
		camera.grab()
		size -= 1

	ret, frame = camera.read()
	return frame if ret == True else None

count = 0
print("OpenCV 로딩 완료")
print("키 입력 준비 완료")

frame = take_picture()
while True:
	# 아래 show에서 picture 윈도를 만들어야 cv2.waitKey()가 작동함
	if frame is not None:
		cv2.imshow("picture", frame)
	if cv2.waitKey(0) == 27:
		break
	else:
		frame = take_picture()
		count += 1
		file_name = "image_5_7" + str(count) + ".jpg"
		cv2.imwrite(file_name, frame)

camera.release()
cv2.destroyAllWindow()
