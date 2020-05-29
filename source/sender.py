import logging

import requests
from requests.exceptions import RequestException


BACKEND_URL = "http://backend:8080/points"
logger = logging.getLogger("source")


def send_data(data):
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