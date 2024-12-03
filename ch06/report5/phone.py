from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/store', methods=['GET'])
def store():
  name = request.args['name'] # name 키에 대한 값 데이터
  tel = request.args['tel'] #'tel' 키에 대한 값 데이터
  
  file = open("./data/phonebook.txt", "a") #추가모드로 phonebook 파일 열기
  data = "%s, %s\n" % (name, tel) #data 변수에 "name, tel\n" 형식으로 저장
  file.write(data)
  file.close()

  return render_template('index.html', msg='저장되었습니다.')

  
@app.route('/search', methods=['post'])
def search():
  name = request.form['name'] # 'name' 키에 대한 데이터

  file = open("./data/phonebook.txt", "r")
  myDict = {}
  # 딕셔너리(myDict)를 만들고 데이터를 "이름":"전화번호" 형식으로 집어넣음
  for line in file.readlines():
    data = line.strip().split(',')  # ','로 구분하여 리스트로 변환
    myDict[data[0]] = data[1] # data[0]=이름, data[1]=전화번호

  file.close()

  # web page에 출력
  if(myDict.get(name) == None):
    return render_template('index.html', alert='저장된 전화번호가 없습니다') # 입력받은 이름이 phonebook.txt에 없으면
  return render_template('index.html', nameData=name, middle='의 전화번호는', telData=myDict[name]) # 입력받은 이름에 해당하는 전화번호와 이름 리턴
    

@app.route('/delete', methods=['GET'])
def delete():
  file = open("./data/phonebook.txt", "w") # 읽기 모드로 열어서 데이터 지우기
  file.write("")
  file.close()
  return render_template('index.html')

@app.route('/print', methods=['GET'])
def printIndex():
  file = open("./data/phonebook.txt", "r")
  myDict = {}
  # 딕셔너리(myDict)를 만들고 데이터를 "이름":"전화번호" 형식으로 집어넣음
  for line in file.readlines():
    data = line.strip().split(',')  # ','로 구분하여 리스트로 변환
    myDict[data[0]] = data[1] # data[0]=이름, data[1]=전화번호

  file.close()

  return render_template('print.html', myDict=myDict) # 딕셔너리 전체 전달



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
