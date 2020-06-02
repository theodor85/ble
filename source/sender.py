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

def make_body_request(source_name, devices_list):
    ''' Функция возвращает тело post-запроса к бэкенду.
    '''
    
    devices = list()
    for device in devices_list:
        devices.append{
            "addr_point": device.addr,
            "rssi": device.rssi,
        }

    return {
        "anchor": source_name,
        "ble_points": points,
    }
