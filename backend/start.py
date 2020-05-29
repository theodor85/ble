import logging
from collections import deque
import json
import time
import asyncio

import aiohttp
from aiohttp import web

from coords import get_device_coords


logger = logging.getLogger("backend")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)

coords_queue = deque()


async def get_points(request):
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

    ws = web.WebSocketResponse()
    await ws.prepare(request)

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
                    }
                )
            await ws.send_json(json.dumps(data))

    return ws


app = web.Application()
app.add_routes([web.post('/points', get_points),
                web.get('/sock', websocket_handler)])

if __name__ == '__main__':
    web.run_app(app)
