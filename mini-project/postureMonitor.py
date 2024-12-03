import cv2
import time
import json
import circuit

file_path_timestamp = "./static/timestamps.json"
file_path_usagetime = "./static/usagetime.json"

# 카메라 및 센서 초기화
faceClassifier = cv2.CascadeClassifier('./haar-cascade-files-master/haarcascade_frontalface_default.xml')
eyeClassifier = cv2.CascadeClassifier('./haar-cascade-files-master/haarcascade_eye.xml')

camera = cv2.VideoCapture(0, cv2.CAP_V4L)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

def append_to_json(file_path, new_data):
  try:
    # 기존 파일 읽기
    with open(file_path, "r") as file:
      data = json.load(file)
  except (FileNotFoundError, json.JSONDecodeError):
    # 파일이 없거나 비어 있으면 빈 리스트로 초기화
    data = []

  # 새 데이터 추가
  data.append(new_data)

  # 파일에 저장 (덮어쓰기)
  with open(file_path, "w") as file:
    json.dump(data, file, indent=4)

# 글로벌 변수 선언
computerUsageStart = 0
computerUsageTime = 0
stopStack = 0

# 초음파 센서 설정
DISTANCE_THRESHOLD = 8  # cm 기준

while True:
  camera.grab()  # 이전 프레임 제거
  # 버퍼에서 현재 카메라가 촬영한 프레임 읽기
  ret, image = camera.read()
  if ret==False:
    print("Frame read failed")
    continue

  # 흑백 이미지 변환 및 탐지
  image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  faces = faceClassifier.detectMultiScale(image_gray)
  eye = eyeClassifier.detectMultiScale(image_gray)

  # 얼굴과 눈이 모두 감지되면
  if len(faces) > 0 and len(eye) > 0:
    print("face and eyes are detected")
    stopStack = 0 # stopStack 초기화
    if computerUsageStart == 0:  # 초기값 설정
      computerUsageStart = time.time()
    for i in range(6): # 초음파 거리 측정 함수 6번 호출 -> 30초
      distance = circuit.ultrasonic_distance() # 거리 측정
      #print("Distance: " + distance +"cm")
      if distance < DISTANCE_THRESHOLD: #임계치(8cm)보다 거리가 작으면
        append_to_json(file_path_timestamp, {"timestamp": time.time()}) # json 파일에 현재 시간 저장
        circuit.controlLED(1) # led 켬
        print("You are too close!")
      else:
        circuit.controlLED(0) # led 끔
      time.sleep(5)  # 초음파 센서 측정 주기 5초

  # 감지되지 않으면
  else:
    print("not detected")
    # 시간 기록중이면
    if computerUsageStart > 0: 
      stopStack += 1 # stopStack 1증가 -> stopStack==5이면 종료
      print("stopstack plus")
      time.sleep(4) # 4초 동안 대기 (한 번에 종료하지 않기 위함)
      # stopStack 이 5번 쌓이면 컴퓨터 사용 종료로 간주 후, 사용시간 계산
      if stopStack >= 5:
        computerUsageEnd = time.time()
        computerUsageTime = computerUsageEnd - computerUsageStart
        print("Computer usage time " + str(computerUsageTime) + "seconds")

        # 사용 시간 데이터를 JSON에 추가
        usage_data = {
            "start": computerUsageStart,
            "end": computerUsageEnd,
            "usage_time": computerUsageTime
        }
        append_to_json(file_path_usagetime, usage_data)
        
        # 변수 초기화
        computerUsageStart = 0 # 사용시작 시간 초기화
        stopStack = 0 # 종료 판단 스택 초기화
  time.sleep(1) # margin

# 종료 처리
GPIO.cleanup()
camera.release()
cv2.destroyAllWindows()