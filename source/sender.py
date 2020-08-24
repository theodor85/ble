''' В модуле реализованы функции для отправки данных на backend
'''

import logging
import json

import requests
from requests.exceptions import RequestException


BACKEND_URL = "http://10.128.14.54:8080/points"
logger = logging.getLogger("source")
ALLOWED_DEVICES = ["ef:33:5d:f3:0a:06", "cd:9b:3d:2b:5e:31", "c5:60:92:2a:81:81"]


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

def make_body_request(source_name, devices_list):
    ''' Функция возвращает тело post-запроса к бэкенду.
    '''

    devices = list()
    for device in devices_list:
        print(f"Устройтво: {device.addr}")
        if device.addr in ALLOWED_DEVICES:
            devices.append({
                "addr_point": device.addr,
                "rssi": device.rssi,
            })

    return {
        "anchor": source_name,
        "ble_points": devices,
    }
