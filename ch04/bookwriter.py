# 쓰기모드로 phonebook.txt 파일 열기
file = open("phonebook.txt", "w")

while True :
        name = input("name>>")  # 이름을 입력받음

        # exit을 입력받으면 반복문 탈출
        if name == "exit":
                break

        tel = input("tel>>")  # 전화번호를 입력받음
        data = "%s, %s\n" % (name, tel) # data변수에 "이름, 전화번호\n" 형식으로 저장
        file.write(data)  # data를 file에 쓴다
file.close()
