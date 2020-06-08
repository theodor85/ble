import logging
import json
import time
import asyncio

import aiohttp
from aiohttp import web

from coords import get_device_coords
from restricted_area_checker import is_restricted_area_violation
from restricted_area_checker import Config, get_restricted_area_size

SEND_TIMEOUT = 3

# настройка логирования
logger = logging.getLogger("backend")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)

# разделяемые данные об устройствах
class DevicesData:

    def __init__(self):
        self._devices_list = list()

    def add_received_data(self, data):
        for dev in data['ble_points']:
            # ищем элемент с этим адресом
            found_flag = False
            for item in self._devices_list:
                if dev['addr_point'] == item['addr']:
                    found_flag = True
                    # обнoвляем пришедшие данные
                    if not item.get(data['anchor']):
                        item[data['anchor']] = list()
                    item[data['anchor']].append({
                        'rssi': dev['rssi'],
                        'violation': is_restricted_area_violation(dev['rssi']),
                    })
                    break
            # если элемент не найден, добавляем новый
            if not found_flag:
                history = list()
                self._devices_list.append({
                    'addr': dev['addr_point'],
                    data['anchor']: history,
                })
                history.append({
                    'rssi': dev['rssi'],
                    'violation': is_restricted_area_violation(dev['rssi']),
                })

    def get_data(self):
        return self._devices_list


devices_data = DevicesData()


async def get_points(request):
    ''' Получает данные о точках (устройтвах)
    '''
    data = await request.json()
    logger.info(f'Получены данные {data}')

    devices_data.add_received_data(data)
    return web.Response(text='OK')

async def websocket_handler(request):
    ''' Принимает соединение по WebSocket и передает
        на fronend данные об устройствах и запретной зоне.
    '''

    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    # отправляем данные о конфигурации запретной зоны
    restr_area_data = {
        "restricted_area": get_restricted_area_size()
    }
    print(f'\nОтправлены данные о запретной зоне: {restr_area_data}\n')
    await ws.send_json(json.dumps(restr_area_data))

    # отправляем данные об устройствах
    while True:
        await asyncio.sleep(SEND_TIMEOUT)

        data = devices_data.get_data()
        print(f'\nОтправлено в браузер: {data}\n')
        await ws.send_json(json.dumps(data))

    return ws


app = web.Application()
app.add_routes([web.post('/points', get_points),
                web.get('/sock', websocket_handler)])

if __name__ == '__main__':
    config = Config()
    web.run_app(app)