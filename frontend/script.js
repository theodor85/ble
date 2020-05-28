var sock = new WebSocket('ws://0.0.0.0:5000/sock');

sock.onopen = function (event) {
    console.log(event);
    console.log('Connection to server started');
};

sock.onclose = function (event) {
    console.log(event);
    if(event.wasClean){
        console.log('Clean connection end');
    } else {
        console.log('Connection broken');
    }
    window.location.assign('/');
};

sock.onerror = function (error) {
    console.log(error);
};

var canvas = document.getElementById('canvas');
var ctx = canvas.getContext("2d");

sock.onmessage = function showMessage(message) {
    var data = JSON.parse(message.data);

    // умножаем на три, т.к. у нас сторона 300х300, а на сервере - 100х100
    console.log(data)
    let x = 3*data.x;
    let y = 3*data.y;

    console.log('x = ' + x + '; y = ' + y)

    ctx.moveTo(x-5, y);
    ctx.arc(x, y, 5, 0, Math.PI*2);
    ctx.stroke();

}

// function draw(){
//     var canvas = document.getElementById('canvas');
    
    

//     if (canvas.getContext){
//         console.log("Inside the function!")
//         var ctx = canvas.getContext("2d");

//         ctx.beginPath();
//         

        
        
//         ctx.stroke();
//     }
//     else{
//         console.log("canvas не поддерживается!")
//     }
//   }