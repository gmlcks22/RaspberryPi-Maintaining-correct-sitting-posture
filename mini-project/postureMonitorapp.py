from flask import Flask, render_template, request, send_from_directory
import json
import os


app = Flask(__name__)

# 브라우저에게, 캐시에 저장된 자바스크립트 파일의 수명을 0으로 성정하여
# 캐시에 저장된 파일을 사용하지 않도록 지시
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

@app.route('/')
def index():
  return render_template('posureMonitor.html') 

@app.route('/static/timestamps.json') # 이벤트 발생 시간
def get_json1():
  # json 파일 반환
  return send_from_directory(os.getcwd() + '/static', 'timestamps.json')

@app.route('/static/usagetime.json') # 사용시간 
def get_json2():
  # json 파일 반환
  return send_from_directory(os.getcwd() + '/static', 'usagetime.json')

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True)