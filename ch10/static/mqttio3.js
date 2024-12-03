let client = null; // mqtt 클라이언트의 역할을 하는 Client 객체를 가리키는 전역변수
let connectionFlag = false; // 연결 상태이면 true
const CLIENT_ID =
  'client-' + Math.floor((1 + Math.random()) * 0x10000000000).toString(16); // 사용자 ID 랜덤 생성

function connect() {
  // 브로커에 접속하는 함수
  if (connectionFlag == true) return;
  let broker = document.getElementById('broker').value;
  let port = 9001;

  document.getElementById('messages').innerHTML +=
    '<span>브로커에 접속 : ' + ' 포트 ' + port + '</span><br/>';
  document.getElementById('messages').innerHTML +=
    '<span>사용자 ID : ' + CLIENT_ID + '</span><br/>';

  client = new Paho.MQTT.Client(broker, Number(port), CLIENT_ID);

  client.onConnectionLost = onConnectionLost;
  client.onMessageArrived = onMessageArrived;

  client.connect({
    onSuccess: onConnect,
  });
}

// 브로커로부터 접속 성공 응답을 받을 떄 호출되는 함수
function onConnect() {
  document.getElementById('messages').innerHTML +=
    '<span>connected' + '</span><br/>';
  connectionFlag = true; // 연결 상태로 설정
}

function subscribe(topic) {
  if (connectionFlag != true) {
    // 연결되지 않은 경우
    alert('연결되지 않았음');
    return false;
  }

  // 구독 신청하였음을 <div> 영역에 출력
  document.getElementById('messages').innerHTML +=
    '<span>구독신청: 토픽 ' + topic + '</span><br/>';

  client.subscribe(topic); // 브로커에 구독 신청
  return true;
}

function publish(topic, msg) {
  if(connectionFlag != true) { // 연결되지 않은 경우
    alert("연결되지 않았음");
    return false;
  }
  client.send(topic, msg, 0, false);
  return true;
}

function unsubscribe(topic) {
  if(connectionFlag != true) return; // 연결되지 않은 경우

  // 구독 신청 취소를 <div> 영역에 출력
  document.getElementById("messages").innerHTML += '<span>구독신청취소: 토픽 ' + topic + '</span><br/>';

  client.unsubscribe(topic, null); // 브로커에 구독 신청 취소
}

// 접속이 끊어졌을 떄 호출되는 함수
function onConnectionLost(responseObject) { // responseObject는 응답 패킷
  document.getElementById("messages").innerHTML +=
    '<span>오류 : 접속 끊어짐</span><br/>';
  if (responseObject.errorCode !== 0) {
    document.getElementById("messages").innerHTML +=
      '<span>오류 : ' + responseObject.errorMessage + '<span><br/>';
  }
  connectionFlag = false; // 연결되지 않은 상태로 설정
}

// 메시지가 도착할 떄 호출되는 함수
function onMessageArrived(msg) {
  console.log('onMessageArrived: ' + msg.payloadString);

  // 도착한 메시지 출력
  document.getElementById('messages').innerHTML +=
    '<span>토픽 : ' +
    msg.destinationName +
    ' | ' +
    msg.payloadString +
    '</span><br/>';
}

//disconnection 버튼이 선택되었을 떄 호출되는 함수
function disconnect() {
  if (connectionFlag == false) return;

  // 켜진 led 끄기
  if(document.getElementById("ledOn").checked == true) {
    client.send('led', "0", 0, false); // led를 끄도록 메시지 전송
    document.getElementById("ledOff").checked = true;
  }
  client.disconnect();
  document.getElementById('messages').innerHTML += '<span>연결종료</span>><br/>';
  connectionFlag = false;
}
