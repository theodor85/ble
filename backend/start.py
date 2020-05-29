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

coords_queue = deque()


async def get_points(request):
    ''' Получает данные о точках (устройтвах), преобразует их в
        координаты, и помещает в очередь для отправки на frontend
    '''
    data = await request.json()

    list_of_devices = list()
    for ble_point in data['ble_points']:
        anchors_data = ble_point['anchors_data']
        r1 = anchors_data[0]['anchor1']
        r2 = anchors_data[1]['anchor2']
        logger.info(f'Получены данные датчиков: r1={r1}; r2={r2}')

        x, y = get_device_coords(r1, r2)

        logger.info(f'Устройство: {ble_point["addr_point"]}; координаты: x={x}; y={y}')
        list_of_devices.append([ble_point["addr_point"], x, y])
    
    coords_queue.appendleft(list_of_devices)
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
    await ws.send_json(json.dumps(restr_area_data))

    # отправляем данные об устройствах
    while True:
        await asyncio.sleep(3)
        try:
            list_of_devices = coords_queue.pop()
        except IndexError:
            continue
        else:
            data = list()
            for device in list_of_devices:
                data.append(
                    {
                        'dev_addr': device[0],
                        'x': device[1],
                        'y': device[2],
                        'violation': is_restricted_area_violation(device[1], device[2])
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
