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
        const device = data[i]
        const signal_anchor1 = device.anchor1[data[i].anchor1.length - 1].rssi;
        const signal_anchor2 = device.anchor2[data[i].anchor2.length - 1].rssi;

        var str_vioation_anchor1 = ''
        if (device.anchor1[data[i].anchor1.length - 1].violation) {
            str_vioation_anchor1 = 'Нарушение anchor1! '
        }
        var str_vioation_anchor2 = ''
        if (device.anchor2[data[i].anchor2.length - 1].violation) {
            str_vioation_anchor2 = 'Нарушение anchor2! '
        }
        var str_vioation = str_vioation_anchor1 + str_vioation_anchor2
        html_list_devices = html_list_devices +
        `
        <a href="#" class="list-group-item list-group-item-action">
          <div class="d-flex w-100 justify-content-between">
            <h5 class="mb-1">${device.addr}</h5>
            <small class="my-red">${str_vioation}</small>
          </div>
          <p class="mb-1">${'anchor1=' + signal_anchor1 + ' дБ; ' + 'anchor2=' + signal_anchor2 + ' дБ'}</p>
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
var restricted_area = 0

function displayDrawing(data){
    
    if (data.restricted_area) {
        restricted_area = data.restricted_area     
    }
    const scale = canvas_height / (max_dB - min_dB)
    ctx.clearRect(0,0,300,300);

    // рисуем запретную зону
    ctx.fillStyle = 'red'
    let zone_y = Math.round( (restricted_area - min_dB) * scale )
    ctx.fillRect(0, zone_y, 300, 300)

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

        //const average_signal = (device.rssi_anchor1 + device.rssi_anchor2) / 2
        const y = Math.round( scale * (device.anchor1[device.anchor1.length-1].rssi - min_dB) )

        // рисуем трек
        ctx.beginPath();
        let path_y = Math.round( scale * (device.anchor1[0].rssi - min_dB) )
        ctx.moveTo(x, path_y)
        device.anchor1.forEach(point => {
            path_y = Math.round( scale * (point.rssi - min_dB) )
            ctx.lineTo(x, path_y)
        });
        ctx.stroke();

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
