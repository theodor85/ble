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

var blink_counter = 0; // счетчик для моргания
var canvas = document.getElementById('draw');
var ctx = canvas.getContext("2d");


function displayDrawingNew(data){

    const canvas_width = 820
    const canvas_height = 580

    const anchor1_x = 236;
    const anchor1_y = 335;
    const anchor1_r = 200;

    const anchor2_x = 584;
    const anchor2_y = 338;
    const anchor2_r = 195;

    const min_dB = -100
    const max_dB = -20
    var restricted_area = 0

    const scale = 5 //canvas_height / (max_dB - min_dB)
    ctx.clearRect(0,0,300,300);
    
    var img = new Image();
    img.src = 'assets/photo_2020-06-08_15-34-51.jpg';

    img.onload = function(){

        blink_counter++; // счетчик для моргания

        let is_violation = false;
        data.forEach(device => {
            if (device.violation){
                is_violation = true
                break;
            }
        });

        ctx.drawImage(img,0,0);
        if ((blink_counter % 2 == 0) && (is_violation)) {
            ctx.strokeStyle = 'red';
        }else {
            ctx.strokeStyle = 'black'; 
        }
            
        // круги, чтобы моргали
        ctx.beginPath();
        ctx.arc(anchor1_x, anchor1_y, anchor1_r, 0, Math.PI*2);
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(anchor2_x, anchor2_y, anchor2_r, 0, Math.PI*2);
        ctx.stroke();

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
            ctx.fillText(device.addr, x+7, y-7)
        }
    };
}

sock.onmessage = function draw(message) {
    var data = JSON.parse(JSON.parse(message.data))
    console.log(data)

    displayDrawingNew(data)
}
