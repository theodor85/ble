''' Модуль сканирует устройства, получает их уровни сигнала, 
    конвертирует их в расстояние до утсройств.
    Затем все эти данные направляет на backend.
    
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


SCAN_TIME = 10


if __name__ == "__main__":
    logger.info("******** Source started!")

    while True:
        # получаем список устройств с уровнями сигналов
        devices_list = scan_anchor(SCAN_TIME)
        
        for device in devices_list:
            logger.debug(f'''*** Найдено устройство: 
                {device.addr} ({device.addrType}), RSSI={device.rssi} dB''')

        # переводим в формат для отправки
        data_for_send = make_body_request(devices_list)

        logger.info(f"Data for send: {data_for_send}")

        # отправляем данные на backend
        send_data(data_for_send)
