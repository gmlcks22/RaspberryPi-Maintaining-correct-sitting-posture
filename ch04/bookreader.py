#읽기모드로 phonebook.txt 파일을 연다.
file = open("phonebook.txt", "r")

#파일 전체를 읽고 각 라인별로 line에 저장
for line in file.readlines(): 
	data = line.strip().split(',') #','로 구분하여 리스트로 변환
	print("이름은 %s, 전화번호는 %s" % (data[0], data[1])) #리스트에 저장된 이름과 전화번호 출력

file.close()
