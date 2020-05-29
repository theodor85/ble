var sock = new WebSocket('ws://0.0.0.0:5000/sock');

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

var canvas = document.getElementById('canvas');
var ctx = canvas.getContext("2d");
var restricted_area = 0
var scale = 3

sock.onmessage = function draw(message) {
    var data = JSON.parse(JSON.parse(message.data))
    console.log(data)
    
    if (data.restricted_area) {
        restricted_area = data.restricted_area     
    }
    ctx.clearRect(0,0,300,300);

    // рисуем запретную зону
    ctx.fillStyle = 'red'
    ctx.fillRect(0, 0, 300, restricted_area*scale)

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
        // умножаем для масштабирования координат
        let x = scale*device.x;
        let y = scale*device.y;
        ctx.beginPath();
        ctx.fillStyle = 'green';
        ctx.arc(x, y, 5, 0, Math.PI*2);
        ctx.fill();

        // делаем надпись
        ctx.fillStyle = 'black';
        ctx.fillText(device.dev_addr, x+7, y-7)
    }

    // отображаем сообщение, если нарушена
    // запретная зона
    let violators = ''
    for (let i = 0; i < data.length; i++) {
        const device = data[i];
        if (device.violation === true){
            violators = violators + device.dev_addr + '; '
        }
    }

    var p_alert = document.getElementById('alert');
    if (violators){
        p_alert.innerHTML= 'ВНИМАНИЕ! Следующие устройства находятся в запретной зоне: ' + violators;
    }else{
        p_alert.innerHTML= ''
    }
}
