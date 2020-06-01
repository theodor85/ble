''' В модуле реализованы функции для отправки данных на backend
'''

import logging
import json

import requests
from requests.exceptions import RequestException


BACKEND_URL = "http://backend:8080/points"
logger = logging.getLogger("source")


def send_data(data):
    ''' Отправка данных на backend '''
    try:
        response = requests.post(BACKEND_URL, data=json.dumps(data))
    except RequestException as req_exception:
        msg = f"******** Backend unreachable! ERROR: {req_exception}"
        logger.error(msg)
    else:
        if response.status_code != 200:
            msg = f"******** Backend returned error status code: {response.status_code}"
            logger.error(msg)
        msg = f"Points data was sent: {data}"
        logger.info(msg)

def make_body_request(devices_list):
    ''' Функция возвращает тело post-запроса к бэкенду.
        На вход получает список устройств (ScanEntry)
    '''
    
    points = list()

    for device in devices_list:
        points.append({
            "addr_point": device.addr,
            "rssi": device.rssi,
        })

    return {"ble_points": points}
