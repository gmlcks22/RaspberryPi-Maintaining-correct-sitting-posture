let client = null; // mqtt 클라이언트의 역할을 하는 Client 객체를 가리키는 전역변수
let connectionFlag = false; // 연결 상태이면 true
const CLIENT_ID =
  'client-' + Math.floor((1 + Math.random()) * 0x10000000000).toString(16); // 사용자 ID 랜덤 생성

function connect() {
  // 브로커에 접속하는 함수
  if (connectionFlag == true) return;
  let broker = document.getElementById('broker').value;
  let port = document.getElementById('port').value;

  document.getElementById('messages').innerHTML +=
    '<span>브로커에 접속 : ' + ' 포트 ' + port + '</span><br/>';
  document.getElementById('messages').innerHTML +=
    '<span>사용자 ID : ' + ' 포트 ' + CLIENT_ID + '</span><br/>';

  client = new Paho.MQTT.Client(broker, Number(port), CLIENT_ID);

  client.onConnectionLost = onConnectionLost;
  client.onMessageArrived = onMessageArrived;

  client.connect({
    onSuccess: onConnect,
  });
}

// 브로커로부터 접속 성공 응답을 받을 떄 호출되는 함수
function onConnect() {
  let topic = document.getElementById('topic').value;
  client.subscribe(topic);

  document.getElementById('messages').innerHTML +=
    '<span>구독신청: 토픽 ' + topic + '</span><br/>';
  connectionFlag = true; //연결 상태로 설정
}

// 접속이 끊어졌을 떄 호출되는 함수
function onConnectionLost(responseObject) {
  document.getElementById('messages').innerHTML +=
    '<span>오류 : 접속 끊어짐</span><br/>';
  if (responseObject.errorCode !== 0) {
    document.getElementById('messages').innerHTML +=
      '<span>오류' + responseObject.errorMessage + '<span><br/>';
  }
  connectionFlag = false; // 연결되지 않은 상태로 설정
}

// 메시지가 도착할 떄 호출되는 함수
function onMessageArrived(msg) {
  console.log('onMessageArrived: ' + msg.payloadString);

  document.getElementById('messages').innerHTML +=
    '<span>토픽 : ' +
    msg.destinationName +
    ' | ' +
    msg.payloadString +
    '</span><br/>';
}

//disconnect 버튼이 선택되었을 떄 호출되는 함수
function disconnection() {
  if (connectionFlag == false) return;
  client.disconnect();
  document.getElementById('messages').innerHTML +=
    '<span>연결종료</span>><br/>';
  connectionFlag = false;
}

