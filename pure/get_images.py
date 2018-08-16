import os
from urllib.parse import urlparse
import asyncio
import aiohttp
import async_timeout
import aiofiles
import motor.motor_asyncio
from PIL import Image

HTTP_TIMEOUT = 10
IMAGE_DIR = './images/'
MONGO_DB = 'images'
MONGO_COLLECTION = 'downloaded'


def get_name(url):
    path = urlparse(url).path
    return os.path.basename(path)


async def fetch(http_session, url):
    async with http_session.get(url) as response:
        return await response.read()


async def download(http_session, mongo_collection, name, url):
    with async_timeout.timeout(HTTP_TIMEOUT):
        response = await fetch(http_session, url)
        filename = os.path.join(IMAGE_DIR, name)
        async with aiofiles.open(filename, mode='wb') as file:
            await file.write(response)
        # Achtung! Sync operation! Brain using needed.
        with Image.open(filename) as image:
            width, height = image.size
        # end of sync operation
        document = {'url': url, 'width': width, 'height': height}
        await mongo_collection.replace_one({'url': url}, document)


async def main(loop, mongo_collection, raw_urls):
    urls = {get_name(url): url for url in raw_urls}
    async with aiohttp.ClientSession(loop=loop) as http_session:
        tasks = [download(http_session, mongo_collection, name, url) for name, url in urls.items()]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    if not os.path.exists(IMAGE_DIR):
        os.mkdir(IMAGE_DIR)

    raw_urls = [
        'http://mindstate.info/favicon.ico',
        'http://mindstate.info/apple-touch-icon.png',
        'http://mindstate.info/apple-touch-icon-precomposed.png',
    ]

    mongo_client = motor.motor_asyncio.AsyncIOMotorClient()
    mongo_collection = mongo_client[MONGO_DB][MONGO_COLLECTION]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop, mongo_collection, raw_urls))

    # if asyncio.ensure_future()
#    pending_tasks = [task for task in asyncio.Task.all_tasks() if not task.done()]
#    loop.run_until_complete(asyncio.gather(*pending_tasks))
#    loop.close()
