import logging
from collections import deque
import json
import time
import asyncio

import aiohttp
from aiohttp import web

from coords import get_device_coords
from restricted_area_checker import is_restricted_area_violation
from restricted_area_checker import Config, get_restricted_area_size


logger = logging.getLogger("backend")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)

devices_queue = deque()


async def get_points(request):
    ''' Получает данные об устройтвах (адрес, уровень сигнала),
        и помещает в очередь для отправки на frontend
    '''
    data = await request.json()

    list_of_devices = list()
    for ble_point in data['ble_points']:
        logger.info(f'Получено Устройство: {ble_point["addr_point"]}; RSSI={ble_point["rssi"]}')
        list_of_devices.append(ble_point)

    devices_queue.appendleft(list_of_devices)
    return web.Response(text='OK')

async def websocket_handler(request):
    ''' Принимает соединение по WebSocket и передает
        на fronend данные об устройствах.
    '''

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # отправляем данные об устройствах
    while True:
        await asyncio.sleep(3)
        try:
            list_of_devices = devices_queue.pop()
        except IndexError:
            continue
        else:
            data = list()
            for device in list_of_devices:
                data.append(
                    {
                        'dev_addr': device["addr_point"],
                        'rssi': device["rssi"],
                        'violation': is_restricted_area_violation(device["rssi"])
                    }
                )
            await ws.send_json(json.dumps(data))

    return ws


app = web.Application()
app.add_routes([web.post('/points', get_points),
                web.get('/sock', websocket_handler)])

if __name__ == '__main__':
    config = Config()
    web.run_app(app)
