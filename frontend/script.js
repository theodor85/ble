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

sock.onmessage = function draw(message) {
    var coords = JSON.parse(JSON.parse(message.data))
    // умножаем на три, т.к. у нас сторона 300х300, а на сервере - 100х100
    let x = 3*coords.x;
    let y = 3*coords.y;
    console.log('x = ' + x + '; y = ' + y)

    ctx.clearRect(0,0,300,300);
    
    ctx.beginPath();
    ctx.fillStyle = 'green';
    ctx.arc(x, y, 5, 0, Math.PI*2);
    ctx.fill();
}
