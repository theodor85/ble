''' Модуль отправляет тестовые данные о положении меток.
    
'''
import logging

from scanner import scan
from sender import send_data, make_body_request
from utils import convert_from_dB_to_meters


logger = logging.getLogger("source")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)


SCAN_TIME = 5


if __name__ == "__main__":
    logger.info("******** Source started!")

    while True:
        # сканируем, получаем список устройств с их децибелами
        devices_list = scan(SCAN_TIME) # list of MyScanEntry

        # конвертируем децибелы в метры
        devices_list_meters = convert_from_dB_to_meters(devices_list)  # list of tuples
        
        # переводим в формат для отправки
        data_for_send = make_body_request(devices_list_meters)

        # отправляем данные на backend
        send_data(data_for_send)
