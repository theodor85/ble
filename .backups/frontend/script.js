var sock = new WebSocket('ws://10.128.14.54:8080/sock');

sock.onopen = function (event) {
    console.log(event);
    console.log('Connection to server started');
};

sock.onclose = function (event) {
    console.log(event);
};

sock.onerror = function (error) {
    console.log(error);
};

function displayDevicesList(data){
    // выводим список устройств
    var div_devices = document.getElementById('devices');
    var html_list_devices = ''
    for (let i = 0; i < data.length; i++) {
        const device = data[i];

        var str_vioation = ''
        if (device.violation) {
            str_vioation = 'Нарушение!'
        }
        html_list_devices = html_list_devices +
        `
        <a href="#" class="list-group-item list-group-item-action">
          <div class="d-flex w-100 justify-content-between">
            <h5 class="mb-1">${device.addr}</h5>
            <small class="my-red">${str_vioation}</small>
          </div>
          <p class="mb-1">${'anchor1=' + device.rssi_anchor1 + ' дБ; ' + 'anchor2=' + device.rssi_anchor2 + ' дБ'}</p>
        </a>
        `
    }
    div_devices.innerHTML = html_list_devices
}

var canvas = document.getElementById('canvas');
var ctx = canvas.getContext("2d");
const canvas_width = 300
const canvas_height = 300
const min_dB = -100
const max_dB = -20

function displayDrawing(data){
    
    ctx.clearRect(0,0,300,300);

    // рисуем anchors
    // anchor1
    ctx.beginPath();
    ctx.fillStyle = 'green';
    ctx.arc(0, 300, 20, 0, Math.PI/2, true);
    ctx.fill();
    // подпись
    ctx.fillStyle = 'black';
    ctx.fillText('Anchor1', 15, 285)

    // anchor2
    ctx.beginPath();
    ctx.fillStyle = 'green';
    ctx.arc(300, 300, 20, 0, Math.PI/2, true);
    ctx.fill();
    // подпись
    ctx.fillStyle = 'black';
    ctx.fillText('Anchor2', 245, 285)

    // рисуем точки
    for (let i = 0; i < data.length; i++) {
        const device = data[i];
        
        points_number = data.length;
        const x = Math.round( canvas_width / (points_number+1) * (i + 1) )

        const scale = canvas_height / (max_dB - min_dB)
        const average_signal = (device.rssi_anchor1 + device.rssi_anchor2) / 2
        const y = Math.round( scale * (average_signal - min_dB) )

        ctx.beginPath();
        ctx.fillStyle = 'green';
        ctx.arc(x, y, 5, 0, Math.PI*2);
        ctx.fill();

        // делаем надпись
        ctx.fillStyle = 'black';
        ctx.fillText(device.addr, x+7, y-7)
    }
}

sock.onmessage = function draw(message) {
    var data = JSON.parse(JSON.parse(message.data))
    console.log(data)

    displayDrawing(data)
    displayDevicesList(data)
}
