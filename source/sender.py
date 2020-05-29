import logging
import json

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

def make_body_request(r_list_anchor1, r_list_anchor2):
    ''' Функция возвращает тело post-запроса к бэкенду.
        На вход получает список с расстояниями от якорей до метки
    '''
    
    points = list()
    
    for point in r_list_anchor1:
        points.append({
            "addr_point": point[0],
            "anchors_data": [
                {"anchor1": point[1]}
            ]
        })
    
    for point in r_list_anchor2:
        for p in points:
            if p["addr_point"] == point[0]:
                p["anchors_data"].append({
                    "anchor2": point[1]
                })
                break

    return {"ble_points": points}
