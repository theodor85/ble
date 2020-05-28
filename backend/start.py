import logging

from aiohttp import web


logger = logging.getLogger("backend")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

async def get_points(request):
    logger.info(f'Data was received! {request}')
    return web.Response(text='OK')


app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle),
                web.post('/points', get_points)])

if __name__ == '__main__':
    web.run_app(app)
