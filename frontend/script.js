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

function displayDevicesList(div_id, data){
    // выводим список устройств
    var div_devices = document.getElementById(div_id);
    var html_list_devices = `<p>${data.anchor}</p>`
    for (let i = 0; i < data.ble_points.length; i++) {
        const device = data.ble_points[i];

        var str_vioation = ''
        if (device.violation) {
            str_vioation = 'Нарушение!'
        }
        html_list_devices = html_list_devices +
        `
        <a href="#" class="list-group-item list-group-item-action">
          <div class="d-flex w-100 justify-content-between">
            <h5 class="mb-1">${device.addr_point}</h5>
            <small class="my-red">${str_vioation}</small>
          </div>
          <p class="mb-1">${device.rssi + ' дБ'}</p>
        </a>
        `
    }
    div_devices.innerHTML = html_list_devices
}

sock.onmessage = function draw(message) {
    var data = JSON.parse(JSON.parse(message.data))
    console.log(data)

    var div_id = ''
    if (data.anchor=='anchor1') {
        div_id = 'devices1'
    }else{
        div_id = 'devices2'
    }
    
    displayDevicesList(div_id, data)

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
