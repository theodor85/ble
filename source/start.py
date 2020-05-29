''' Модуль отправляет тестовые данные о положении меток.
    
'''
import logging

from scanner import scan_anchor
from sender import send_data, make_body_request
from converter import convert_from_dB_to_meters


logger = logging.getLogger("source")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)


SCAN_TIME = 3


if __name__ == "__main__":
    logger.info("******** Source started!")

    while True:
        # получаем список устройств с уровнями сигналов для каждого якоря
        devices_list_anchor1 = scan_anchor('anchor1', SCAN_TIME)
        devices_list_anchor2 = scan_anchor('anchor2', SCAN_TIME) # list of MyScanEntry

        # конвертируем децибелы в метры
        devices_list_meters_anchor1 = convert_from_dB_to_meters(devices_list_anchor1)
        devices_list_meters_anchor2 = convert_from_dB_to_meters(devices_list_anchor2)

        # переводим в формат для отправки
        data_for_send = make_body_request(
            devices_list_meters_anchor1,
            devices_list_meters_anchor2)

        logger.info(f"Data for send: {data_for_send}")

        # отправляем данные на backend
        send_data(data_for_send)
