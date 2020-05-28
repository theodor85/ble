import logging

from aiohttp import web

from coords import get_device_coords


logger = logging.getLogger("backend")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)


async def get_points(request):
    data = await request.json()
    

    anchors_data = data['ble_points'][0]['anchors_data']
    r1 = anchors_data[0]['anchor1']
    r2 = anchors_data[1]['anchor2']
    logger.info(f'Получены данные датчиков: r1={r1}; r2={r2}')

    x, y = get_device_coords(r1, r2)

    logger.info(f'Определены координаты точки: x={x}; y={y}')
    
    return web.Response(text='OK')


app = web.Application()
app.add_routes([web.post('/points', get_points)])

if __name__ == '__main__':
    web.run_app(app)
