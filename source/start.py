''' Модуль отправляет тестовые данные о положении меток.
    Позже может быть замменен на библиотеки, работающие с реальными данными.
'''

import logging
import time
import json

import requests
from requests.exceptions import RequestException


TEST_DATA = [
    [51, 51], # 1
    [63, 45], # 2
    [76, 42], # 3
    [89, 45], # 4
    [86, 58], # 5
    [84, 72], # 6
    [86, 86], # 7
    [89, 100], # 8
    [76, 99], # 9
    [67, 92], # 10
    [64, 78], # 11
    [64, 64], # 12
    [50, 67], # 13
    [45, 63], # 14
]

BACKEND_URL = "http://backend:8080/points"
SENDING_INTERVAL = 3 # сек

logger = logging.getLogger("source")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)

def make_body_request(r_list):
    ''' Функция возвращает тело post-запроса к бэкенду.
        На вход получает список с расстояниями от якорей до метки
    '''
    return {
        "ble_points": [
            {
                "id_point": "point1",
                "anchors_data": [
                    {
                        "anchor1":r_list[0]
                    },
                    {
                        "anchor2":r_list[1]
                    },
                ]
            },
        ]
    }


if __name__ == "__main__":
    logger.info("******** Source started!")

    i = 0
    while True:
        time.sleep(SENDING_INTERVAL)
        try:
            body = make_body_request(TEST_DATA[i])
            response = requests.post(BACKEND_URL, data=json.dumps(body))
        except RequestException as req_exception:
            msg = f"******** Backend unreachable! ERROR: {req_exception}"
            logger.error(msg)
        else:
            if response.status_code != 200:
                msg = f"******** Backend returned error status code: {response.status_code}"
                logger.error(msg)
            msg = f"Points data was sent: {TEST_DATA[i]}"
            logger.info(msg)
        i += 1
        if i >= 14:
            i = 0
