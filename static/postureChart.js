let currentUnit = 'hour'; // 차트의 기본 단위는 'hour'

function fetchDataAndDrawCharts() {
  // timestamps.json 데이터를 가져와서 처리
  fetch('/static/timestamps.json')
    .then(response => response.json())
    .then(timestamps => {
      // currentUnit에 따라 데이터를 그룹화
      const groupedTimestamps =
        currentUnit === 'hour'
          ? groupByHour(timestamps, 'timestamp')
          : groupByMinute(timestamps, 'timestamp');

      // 차트 그리기: 특정 이벤트 횟수
      drawChart(
        'eventCanvas',
        '시간대별 이벤트 발생 횟수',
        groupedTimestamps.labels,
        groupedTimestamps.data,
        'rgba(255, 99, 132, 0.2)',
        'rgba(255, 99, 132, 1)'
      );
    })
    .catch(error => {
      console.error('Error fetching timestamps:', error);
    });

  // usagetime.json 데이터를 가져와서 처리
  fetch('/static/usagetime.json')
    .then(response => response.json())
    .then(usagetime => {
      // currentUnit에 따라 데이터를 그룹화
      const groupedUsagetime =
        currentUnit === 'hour'
          ? groupByHour(usagetime, 'usage_time')
          : groupByMinute(usagetime, 'usage_time');

      // 차트 그리기: 사용 시간
      drawChart(
        'usageCanvas',
        '시간대별 총 사용 시간(분)',
        groupedUsagetime.labels,
        groupedUsagetime.data,
        'rgba(75, 192, 192, 0.2)',
        'rgba(75, 192, 192, 1)'
      );
    })
    .catch(error => {
      console.error('Error fetching usagetime:', error);
    });
}

// 시간대별로 데이터를 그룹화하는 함수
function groupByHour(data, key) {
  const groupedData = {};

  data.forEach(item => {
    const timestamp = key === 'timestamp' ? item.timestamp : item.start;
    const date = new Date(timestamp * 1000);
    const hour = date.getHours(); // 0 ~ 23
    const label = `${hour}:00`;

    if (!groupedData[label]) {
      groupedData[label] = 0;
    }

    if (key === 'usage_time') {
      groupedData[label] += item.usage_time / 60;
    } else if (key === 'timestamp') {
      groupedData[label] += 1;
    }
  });

  const labels = Object.keys(groupedData).sort((a, b) => parseInt(a) - parseInt(b));
  const dataArray = labels.map(label => groupedData[label]);

  return { labels, data: dataArray };
}

// 분별로 데이터를 그룹화하는 함수
function groupByMinute(data, key) {
  const groupedData = {};

  data.forEach(item => {
    const timestamp = key === 'timestamp' ? item.timestamp : item.start;
    const date = new Date(timestamp * 1000);
    const hour = date.getHours(); // 시간 0 - 23
    const minute = date.getMinutes(); // 0 - 59
    const label = `${hour}시 ${minute}분`;

    if (!groupedData[label]) {
      groupedData[label] = 0;
    }

    if (key === 'usage_time') {
      groupedData[label] += item.usage_time / 60;
    } else if (key === 'timestamp') {
      groupedData[label] += 1;
    }
  });

  const labels = Object.keys(groupedData).sort((a, b) => parseInt(a) - parseInt(b));
  const dataArray = labels.map(label => groupedData[label]);

  return { labels, data: dataArray };
}


// 차트 객체를 저장하기 위한 전역 변수
let charts = {};
// 차트를 그리는 함수
function drawChart(canvasId, title, labels, data, bgColor, borderColor) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) {
    console.error(`Canvas with id ${canvasId} not found.`);
    return;
  }

  const ctx = canvas.getContext('2d');

  // 기존 차트가 있으면 삭제
  if (charts[canvasId]) {
    charts[canvasId].destroy();
  }

  // 새 차트 생성
  charts[canvasId] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: title,
          data: data,
          backgroundColor: bgColor,
          borderColor: borderColor,
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        x: {
          display: true,
          title: { display: true, text: '시간대' },
        },
        y: {
          display: true,
          title: { display: true, text: '값' },
          beginAtZero: true,
        },
      },
    },
  });
}

// 단위 변경 버튼 이벤트
document.getElementById('toggleUnitButton').addEventListener('click', () => {
  currentUnit = currentUnit === 'hour' ? 'minute' : 'hour';
  document.getElementById('toggleUnitButton').innerText =
    currentUnit === 'hour' ? '단위를 분 단위로 변경' : '단위를 시간 단위로 변경';

  // 데이터를 다시 가져오고 차트를 갱신
  fetchDataAndDrawCharts();
});

// 페이지 로드 시 초기 데이터 로드 및 차트 그리기
fetchDataAndDrawCharts();
