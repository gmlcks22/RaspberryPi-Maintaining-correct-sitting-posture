file = open("phonebook.txt", "r")	# 파일을 읽기모드로 열기
myDict = {}

# 딕셔너리(myDict)를 만들고 데이터를 "이름":"전화번호"형식으로 집어넣음
for line in file.readlines():	# 파일 전체를 읽고, 각 라인별로 line에 저장
	data = line.strip().split(',')	# ','로 구분하여 리스트로 변환
	myDict[data[0]] = data[1]	# data[0]=이름, data[1]=전화번호

#검색
while True:
	name = input("검색할 이름>>")
	if name == "exit":	# exit을 입력받으면 반복문 탈출
		print("검색을 끝냅니다.")
		break
	elif(myDict.get(name) == None):	# 입력받은 이름이 딕셔너리에 없으면
		print("%s는 없음" % (name))
	else:	# 딕셔너리에 있는 키 값(이름)을 입력받으면
		print("%s의 전화번호는 %s" % (name, myDict[name]))	#key(이름), 딕셔너리 원소(전화번호) 출력

file.close()	

