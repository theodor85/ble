## BLE

### Requirements

    Docker version 19.03.8-ce
    docker-compose version 1.25.5

### Запуск

    git clone https://github.com/theodor85/ble.git
    cd ble
    docker-compose up

Первый запуск занимает много времени, т.к. docker загружает необходимые образы.

Система поднимается на адресе:

    http://0.0.0.0:8000/

### Конфигурирование запретной зоны

В файле `backend/config.conf` необходимо указать строку

    restricted_area = <размер зоны>

Размер зоны указывается в метрах. Сделано допущение, что вся территория равна 100х100 м, поэтому размер зоны может быть в пределах от 0 до 100 м.
